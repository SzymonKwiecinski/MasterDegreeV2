import pulp

# Define the problem data
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

# Create the problem
problem = pulp.LpProblem("Seaport_Operations", pulp.LpMinimize)

# Define decision variables
amount = pulp.LpVariable.dicts('Amount', range(T), lowBound=0, cat='Integer')
crane = pulp.LpVariable.dicts('Crane', range(T), lowBound=0, upBound=num_cranes, cat='Integer')
inventory = pulp.LpVariable.dicts('Inventory', range(T+1), lowBound=0, upBound=max_container, cat='Integer')

# Initial inventory
inventory[0] = init_container

# Objective function: Minimize total cost
problem += pulp.lpSum(unload_costs[t] * amount[t] + crane_cost * crane[t] + holding_cost * inventory[t+1] for t in range(T))

# Constraints
for t in range(T):
    # Unloading capacity constraint
    problem += amount[t] <= unload_capacity[t], f"UnloadCapacity_{t}"
    
    # Inventory balance constraint
    problem += inventory[t] + amount[t] - demands[t] == inventory[t+1], f"InventoryBalance_{t}"
    
    # Demand fulfillment constraint
    problem += crane[t] * crane_capacity >= demands[t], f"CranesCapacity_{t}"
    
# End conditions
problem += inventory[T] == 0, f"FinalInventory"

# Solve the problem
problem.solve()

# Extract results
containers_unloaded = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(crane[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')