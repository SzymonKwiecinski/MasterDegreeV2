import pulp

# Load data
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

# Extracting values from the data
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

# Problem
problem = pulp.LpProblem("Seaport_Optimization", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacity[t], cat='Integer') for t in range(T)]
cranes = [pulp.LpVariable(f'cranes_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(T)]
stored = [pulp.LpVariable(f'stored_{t}', lowBound=0, upBound=max_container, cat='Integer') for t in range(T)]

# Objective: Minimize costs
problem += pulp.lpSum([
    unload_costs[t] * amount[t] + crane_cost * cranes[t] + holding_cost * stored[t] for t in range(T)
])

# Constraints
# Initial stored containers
problem += (amount[0] + init_container - demands[0] - cranes[0] * crane_capacity == stored[0])

# Demand and storage balance constraints
for t in range(1, T):
    problem += (stored[t-1] + amount[t] - demands[t] - cranes[t] * crane_capacity == stored[t])

# End of period storage constraint
problem += stored[T-1] == 0

# Solve
problem.solve()

# Output
output = {
    "containers_unloaded": [round(pulp.value(amount[t])) for t in range(T)],
    "cranes_rented": [round(pulp.value(cranes[t])) for t in range(T)],
    "total_cost": round(pulp.value(problem.objective))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')