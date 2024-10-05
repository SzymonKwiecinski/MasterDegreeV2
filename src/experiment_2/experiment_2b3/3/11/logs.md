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

#### Define data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

#### Extract variables
T = data['T']
Deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Initialize the LP problem
problem = pulp.LpProblem("Production_Inventory_Planning", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", (i for i in range(1, T + 1)), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", (i for i in range(1, T + 1)), lowBound=0, cat='Continuous')

#### Objective function: Minimize total cost
problem += pulp.lpSum([
    storage_cost * inventory[i] + 
    switch_cost * pulp.lpSum([x[i] - x[i-1] for i in range(2, T + 1)])
    for i in range(1, T + 1)
])

#### Constraints
problem += inventory[1] == x[1] - Deliver[0]  #### For the first month
for i in range(1, T):
    problem += inventory[i + 1] == inventory[i] + x[i + 1] - Deliver[i]

#### Solve the problem
problem.solve()

#### Collect results
production_plan = [pulp.value(x[i]) for i in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

#### Print results
print({
    "x": production_plan,
    "cost": total_cost
})
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

