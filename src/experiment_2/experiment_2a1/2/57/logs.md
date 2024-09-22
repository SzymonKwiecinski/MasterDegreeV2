# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP

PROBLEM INFO:

- A seaport unloads shipping containers off of rail cars, holds them in its yard on a transport system, and then loads them onto ships.
- The demand \var{demand_{t}} for containers by ships varies every month, and this demand must be fulfilled.
- The unloading cost \var{unload_cost_{t}} per container indicates how much it costs to unload a single container from the rail car.
- The unloading capacity \var{unload_capacity_{t}} specifies the maximum number of containers that can be unloaded in a month.
- For each container kept in the yard until the subsequent month, there is a holding cost of $\var{holding_cost}.
- Due to space limitations, the yard can store a maximum of \var{max_container} containers at the end of any month.
- Initially, at the start of the first month, the yard has \var{init_container} containers.
- The yard should not contain any containers after the end of the last month.
- Additionally, loading containers onto ships necessitates the rental of cranes.
- A maximum of \var{num_cranes} cranes can be rented each month, each having a capacity to load \var{crane_capacity} containers.
- It costs \var{crane_cost} for each crane.

INPUT FORMAT: 

{
    "demands": [demand_{t} for t in 1, ..., T],
    "unload_costs": [unload_cost_{t} for t in 1, ..., T],
    "unload_capacity": [unload_capacity_{t} for t in 1, ..., T],
    "holding_cost": holding_cost,
    "max_container": max_container,
    "init_container": init_container,
    "num_cranes": num_cranes,
    "crane_capacity": crane_capacity,
    "crane_cost": crane_cost,
}

OBJECTIVE: Determine a strategy to minimize costs from unloading, storage, and crane rentals over the period.

OUTPUT INFO:

- \var{amount_{t}} indicates the number of containers unloaded for each month.
- \var{crane_{t}} specifies the number of cranes rented for each month.
- \var{total_cost} shows the total cost of the company over the period.

OUTPUT FORMAT:

{
    "containers_unloaded": [amount_{t} for t in 1, ..., T],
    "cranes_rented": [crane_{t} for t in 1, ..., T],
    "total_cost": total_cost
}

</DESCRIPTION>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

#### Parameters
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

#### Create the problem variable
problem = pulp.LpProblem("Seaport_Operation_Optimization", pulp.LpMinimize)

#### Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Continuous')  #### containers unloaded each month
cranes = pulp.LpVariable.dicts("cranes", range(T), lowBound=0, upBound=num_cranes, cat='Integer')  #### cranes rented each month
inventory = pulp.LpVariable.dicts("inventory", range(T + 1), lowBound=0, upBound=max_container, cat='Continuous')  #### containers in yard

#### Objective function
total_cost = pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)]) + \
             pulp.lpSum([holding_cost * inventory[t] for t in range(T)]) + \
             pulp.lpSum([crane_cost * cranes[t] for t in range(T)])
problem += total_cost

#### Constraints
#### Initial inventory
problem += (inventory[0] == init_container)

#### Inventory balance and capacity constraints
for t in range(T):
    problem += (inventory[t] + amount[t] - demands[t] == inventory[t + 1], f"Balance_{t}")
    problem += (amount[t] <= unload_capacity[t], f"Unload_Capacity_{t}")
    problem += (inventory[t + 1] <= max_container, f"Max_Container_{t + 1}")

#### Crane capacity constraints
for t in range(T):
    problem += (cranes[t] * crane_capacity >= demands[t], f"Cranes_Capacity_{t}")

#### Non-negativity and capacity constraints for cranes
for t in range(T):
    problem += (cranes[t] <= num_cranes, f"Max_Cranes_{t}")

#### Ending inventory must be zero
problem += (inventory[T] == 0, "End_Inventory")

#### Solve the problem
problem.solve()

#### Extract results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [cranes[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

#### Output results
results = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')
```

