import pulp

# Parse input data
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
unload_capacities = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Create the problem
problem = pulp.LpProblem("Seaport_Container_Loading", pulp.LpMinimize)

# Decision variables
unload_vars = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacities[t], cat='Integer') for t in range(T)]
crane_vars = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(T)]
yard_inventory = [pulp.LpVariable(f'inventory_{t}', lowBound=0, upBound=max_container, cat='Integer') for t in range(T)]

# Objective function
problem += pulp.lpSum(unload_costs[t] * unload_vars[t] for t in range(T)) \
           + pulp.lpSum(holding_cost * yard_inventory[t] for t in range(T)) \
           + pulp.lpSum(crane_cost * crane_vars[t] for t in range(T))

# Constraints
problem += (yard_inventory[0] == init_container + unload_vars[0] - demands[0] - crane_vars[0] * crane_capacity, "Initial_inventory_balance")

for t in range(1, T):
    problem += (yard_inventory[t] == yard_inventory[t-1] + unload_vars[t] - demands[t] - crane_vars[t] * crane_capacity, f"Inventory_balance_{t}")

problem += (yard_inventory[T-1] == 0, "Final_inventory_balance")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "containers_unloaded": [int(unload_vars[t].varValue) for t in range(T)],
    "cranes_rented": [int(crane_vars[t].varValue) for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')