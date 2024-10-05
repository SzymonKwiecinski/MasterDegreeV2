import pulp

# Data provided
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

# Unpacking the data
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

# Define the optimization problem
problem = pulp.LpProblem('Seaport_Operation', pulp.LpMinimize)

# Decision variables
containers_unloaded = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacity[t], cat='Integer') for t in range(T)]
cranes_rented = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(T)]
containers_held = [pulp.LpVariable(f'hold_{t}', lowBound=0, upBound=max_container, cat='Integer') for t in range(T)]

# Objective function
unloading_cost = pulp.lpSum([unload_costs[t] * containers_unloaded[t] for t in range(T)])
crane_cost_total = pulp.lpSum([crane_cost * cranes_rented[t] for t in range(T)])
holding_cost_total = pulp.lpSum([holding_cost * containers_held[t] for t in range(T)])
problem += unloading_cost + crane_cost_total + holding_cost_total

# Constraints
problem += containers_held[0] == init_container + containers_unloaded[0] - demands[0] - crane_capacity * cranes_rented[0]
for t in range(1, T):
    problem += containers_held[t] == containers_held[t-1] + containers_unloaded[t] - demands[t] - crane_capacity * cranes_rented[t]
problem += containers_held[T-1] == 0

# Solve the problem
problem.solve()

# Collecting the results
output = {
    "containers_unloaded": [pulp.value(containers_unloaded[t]) for t in range(T)],
    "cranes_rented": [pulp.value(cranes_rented[t]) for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')