import pulp

# Data input
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

# Problem initialization
problem = pulp.LpProblem("Seaport_Optimization", pulp.LpMinimize)

# Decision variables
T = data['T']
amount = pulp.LpVariable.dicts("amount", range(T), 0, None, pulp.LpInteger)
cranes = pulp.LpVariable.dicts("cranes", range(T), 0, data['NumCranes'], pulp.LpInteger)
containers = pulp.LpVariable.dicts("containers", range(T+1), 0, data['MaxContainer'], pulp.LpInteger)

# Objective function
problem += pulp.lpSum([amount[t] * data['UnloadCosts'][t] for t in range(T)]) + \
           pulp.lpSum([cranes[t] * data['CraneCost'] for t in range(T)]) + \
           pulp.lpSum([containers[t] * data['HoldingCost'] for t in range(T)])

# Initial containers
problem += containers[0] == data['InitContainer']

# Constraints
for t in range(T):
    # Unloading constraints
    problem += amount[t] <= data['UnloadCapacity'][t]

    # Crane and loading constraints
    problem += cranes[t] * data['CraneCapacity'] >= data['Demands'][t]

    # Balance constraints
    problem += containers[t+1] == containers[t] + amount[t] - data['Demands'][t]

# End of period containers should be zero
problem += containers[T] == 0

# Solve the problem
problem.solve()

# Prepare output
output = {
    "containers_unloaded": [pulp.value(amount[t]) for t in range(T)],
    "cranes_rented": [pulp.value(cranes[t]) for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')