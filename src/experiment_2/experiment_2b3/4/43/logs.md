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
To solve this linear programming problem, we'll use the PuLP library in Python. The goal is to maximize the total profit for the month by determining the optimal production quantities for each product while adhering to the constraints provided.

Here's how we can do it:

```python
import pulp

#### Input data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Extracting data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']
M = len(prices)  #### Number of products
N = len(available)  #### Number of raw materials

#### Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables: amount of each product to produce
amount_vars = [pulp.LpVariable(f'amount_{j+1}', lowBound=0, cat='Continuous') for j in range(M)]

#### Objective function: maximize total profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amount_vars[j] for j in range(M)])
problem += profit

#### Constraints: raw material availability
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount_vars[j] for j in range(M)]) <= available[i]

#### Constraints: forecasted maximum demand
for j in range(M):
    problem += amount_vars[j] <= demands[j]

#### Solve the problem
problem.solve()

#### Collect results
amount = [pulp.value(amount_var) for amount_var in amount_vars]
total_profit = pulp.value(problem.objective)

#### Output
output = {
    "amount": amount,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

In this code:
- We first parse the input JSON to extract the required data.
- We define a linear programming problem with PuLP.
- We then set up the decision variables representing how much of each product to produce.
- We define the objective function to maximize profit, computed as the difference between prices and costs for each product multiplied by the production amount.
- We add constraints for raw material availability and maximum demand.
- Finally, we solve the problem and print the results, including the total profit and quantities of each product produced to maximize profit.

