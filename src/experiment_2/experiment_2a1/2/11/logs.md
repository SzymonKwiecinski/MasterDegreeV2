# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 
- A company must deliver \var{deliver_i} units of its product at the end of the \var{i}_th month.
- Material produced during a month can be delivered either at the end of the same month or can be stored as inventory and delivered at the end of a subsequent month.
- There is a storage cost of \var{storage_cost} dollars per month for each unit of product held in inventory. 
- The year begins with zero inventory. 
- If the company produces \var{x_i} units in month \var{i} and \var{x_{i+1}} units in month \var{i}+1, it incurs a cost of \var{switch_cost} |\var{x_{i+1}} - \var{x_i}|  dollars, reflecting the cost of switching to a new production level. 
- Assume that inventory left at the end of the year has no value and does not incur any storage cost.
- The company wants to minimize the total cost of the production and inventory schedule over the next \var{T} months.

INPUT FORMAT: 

{
    "deliver": [deliver_i for i in 1, ..., T],
    "storage_cost": storage_cost,
    "switch_cost": switch_cost,
}

OBJECTIVE: Minimize the total cost of the production and inventory schedule over the whole period.

OUTPUT INFO:

- \var{x_i} is the number of units produced in month \var{i}.

OUTPUT FORMAT:

{
    "x": [x_i for i in 1, ..., T],
    "cost": cost,
}

</DESCRIPTION>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

#### Extracting data from the input
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Create the problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(T), lowBound=0, cat='Continuous')

#### Objective function
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
             pulp.lpSum(switch_cost * abs(x[i] - x[i + 1]) for i in range(T - 1)) + \
             pulp.lpSum(x[i] for i in range(T))  #### total production to meet demands
objective = pulp.lpSum(total_cost)
problem += objective 

#### Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliveries[i] + inventory[i] == 0  #### first month
    else:
        problem += x[i] - deliveries[i] + inventory[i] == inventory[i - 1]  #### subsequent months

#### Ending inventory has no value
problem += inventory[T - 1] == 0

#### Solve the problem
problem.solve()

#### Collect results
production_schedule = [x[i].varValue for i in range(T)]
total_cost_value = pulp.value(problem.objective)

#### Output format
output = {
    "x": production_schedule,
    "cost": total_cost_value,
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')
```

