# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We suppose that some products can be produced, each of them passing through several stages.
- Necessary time to produce 1 unit of product \var{k} is \var{produce_time_{k, s}} hours for stage \var{s}.
- Availability in working hours is \var{time_{s}} for stage \var{s}. 
- The unitary profits for product \var{k} is \var{profit_{k}}.

INPUT FORMAT:

{
	"produce_time": [[produce_time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"available_time": [time_{s} for s in 1,...,S],
	"profit": [profit_{k} for k in 1,...,K]
}


OBJECTIVE: Determine the quantities to be produced such that all the production constraints are satisfied and the profit is maximized.

OUTPUT INFO:

- \var{quantity} represents the production quantity for each product

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this linear programming problem, we will use the PuLP library in Python. The goal is to determine the optimal production quantities for each product in order to maximize profit while satisfying the production constraints.

Here's the Python code to solve the problem:

```python
import pulp

#### Parse the input data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Create variables for the quantity of each product to produce
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

#### Set objective function to maximize total profit
problem += pulp.lpSum(data['Profit'][k] * quantities[k] for k in range(data['NumProducts']))

#### Add constraints for each machine's available time
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * quantities[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s]

#### Solve the problem
problem.solve()

#### Extract the solution
solution = {
    "quantity": [pulp.value(quantities[k]) for k in range(data['NumProducts'])]
}

print(solution)

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This code snippet sets up and solves a linear programming problem to determine the optimal production quantities for maximizing profit subject to production time constraints. The output includes the quantities of each product to produce and the objective value, which represents the maximum profit.

