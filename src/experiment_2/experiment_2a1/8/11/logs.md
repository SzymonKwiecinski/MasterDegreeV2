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

#### Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

#### Extracting parameters
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Initialize the problem
problem = pulp.LpProblem("Production_Inventory_Schedule", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("Produce", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

#### Objective function
total_cost = pulp.lpSum(switch_cost * pulp.lpAbs(x[i] - x[i + 1]) for i in range(T - 1)) 
                        + pulp.lpSum(storage_cost * inventory[i] for i in range(T))

problem += total_cost

#### Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] + inventory[i] == 0  #### First month
    else:
        problem += x[i] - deliver[i] + inventory[i] - inventory[i - 1] == 0  #### Following months

#### End of the year inventory should not incur any cost
problem += inventory[T - 1] == 0

#### Solve the problem
problem.solve()

#### Output results
result_x = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

output = {
    "x": result_x,
    "cost": cost,
}

print(f' (Objective Value): <OBJ>{cost}</OBJ>')
```

