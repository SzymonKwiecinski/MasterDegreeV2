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

#### Input data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

#### Extract data
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacities = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

#### Create the optimization problem
problem = pulp.LpProblem("Seaport_Cost_Minimization", pulp.LpMinimize)

#### Decision Variables
amounts = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
inventory = pulp.LpVariable.dicts("inventory", range(T+1), lowBound=0, upBound=max_container, cat='Integer')

#### Initial inventory
inventory[0] = init_container

#### Objective Function: Minimize total costs
total_cost = pulp.lpSum([amounts[t] * unload_costs[t] for t in range(T)]) + \
              pulp.lpSum([inventory[t] * holding_cost for t in range(T)]) + \
              pulp.lpSum([cranes[t] * crane_cost for t in range(T)])

problem += total_cost

#### Constraints
for t in range(T):
    #### Demand fulfillment
    problem += (amounts[t] - demands[t] + (inventory[t] if t == 0 else inventory[t-1]) <= 0, f"demand_fulfillment_{t}")

    #### Unloading capacity
    problem += (amounts[t] <= unload_capacities[t], f"unloading_capacity_{t}")

    #### Crane loading capacity
    problem += (cranes[t] * crane_capacity >= demands[t] - (inventory[t] if t == 0 else inventory[t-1]), f"crane_capacity_{t}")

    #### Inventory balance
    if t < T - 1:
        problem += (inventory[t+1] == (inventory[t] + amounts[t] - demands[t]), f"inventory_balance_{t}")

#### End of last month, inventory must be zero
problem += (inventory[T] == 0, "final_inventory")

#### Solve the problem
problem.solve()

#### Retrieve results
containers_unloaded = [int(amounts[t].varValue) for t in range(T)]
cranes_rented = [int(cranes[t].varValue) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

#### Output
result = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')
```

