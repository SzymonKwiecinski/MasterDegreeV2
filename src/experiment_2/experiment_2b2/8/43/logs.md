# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- Wild Sports produces \var{M} different products using \var{N} different raw materials.
- The company has \var{available_{i}} of raw material \var{i} available.
- Product \var{j} requires \var{req_{i,j}} units of material \var{i} per unit produced.
- Product \var{j} has a selling price of \var{price_j} per unit.
- Product \var{j} has a production cost of \var{cost_j} per unit produced.
- Product \var{j} has a forecasted maximum demand of \var{demand_j} for the month.

INPUT FORMAT: 

{
    "available": [available_{i} for i in 1, ..., N],
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M],
    "costs": [cost_{j} for j in 1, ..., M],
    "demands": [demand_{j} for j in 1, ..., M]
}

OBJECTIVE: How many of each product should the sports produce in order to maximize its profit for the month?

OUTPUT INFO:

- the amount of each product produced \var{amount_{j}}.
- \var{total_profit} shows the total profit of the company for the month.

OUTPUT FORMAT:

{
    "amount": [amount_{j} for j in 1, ..., M],
    "total_profit": total_profit
}

</DESCRIPTION>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem, we will use the Pulp library to set up a linear programming model that maximizes profit. The goal is to determine how much of each product to produce given the constraints on raw materials, production costs, and demand.

```python
import pulp

#### Define the data
data = {
    "available": [240000, 8000, 75000],
    "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    "prices": [40, 38, 9],
    "costs": [30, 26, 7],
    "demands": [10000, 2000, 10000]
}

#### Unpack the data
available = data["available"]
requirements = data["requirements"]
prices = data["prices"]
costs = data["costs"]
demands = data["demands"]

#### Number of products and materials
M = len(prices)  #### Number of products
N = len(available)  #### Number of materials

#### Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
x = [pulp.LpVariable(f'product_{j}', lowBound=0, upBound=demands[j], cat='Integer') for j in range(M)]

#### Add objective function (maximize profit)
profit = sum((prices[j] - costs[j]) * x[j] for j in range(M))
problem += profit

#### Add constraints for raw materials
for i in range(N):
    problem += sum(requirements[j][i] * x[j] for j in range(M)) <= available[i]

#### Solve the problem
problem.solve()

#### Collect the results
amount_produced = [pulp.value(x[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

#### Print the solution
print({
    "amount": amount_produced,
    "total_profit": total_profit
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

