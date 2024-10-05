import pulp

# Data from JSON
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

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

# Define the problem
problem = pulp.LpProblem("SeaportOptimization", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacities[t], cat='Integer') for t in range(T)]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(T)]
yard_inventory = [pulp.LpVariable(f'yard_inventory_{t}', lowBound=0, upBound=max_container, cat='Integer') for t in range(T)]

# Objective function
problem += pulp.lpSum([unload_costs[t] * amount[t] + crane_cost * crane[t] + holding_cost * yard_inventory[t] 
                       for t in range(T)])

# Constraints
# Initial inventory constraint
problem += yard_inventory[0] == init_container + amount[0] - crane[0] * crane_capacity

# Monthly flow constraints
for t in range(1, T):
    problem += yard_inventory[t] == yard_inventory[t-1] + amount[t] - crane[t] * crane_capacity

# Demand fulfillment constraints
for t in range(T):
    problem += crane[t] * crane_capacity >= demands[t]

# End of last month should have no containers
problem += yard_inventory[T-1] == 0

# Solve the problem
problem.solve()

# Outputs
containers_unloaded = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(crane[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')