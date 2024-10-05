import pulp

# Given data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Constants
K = len(data['demand'])  # Number of industries
T = 5  # Number of years

# Create a Linear Programming problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision variables
produce = [[pulp.LpVariable(f'produce_{k}_{t}', lowBound=0) for t in range(T)] for k in range(K)]
buildcapa = [[pulp.LpVariable(f'buildcapa_{k}_{t}', lowBound=0) for t in range(T)] for k in range(K)]
stockhold = [[pulp.LpVariable(f'stockhold_{k}_{t}', lowBound=0) for t in range(T+1)] for k in range(K)]

# Objective function: Maximize total manpower requirement over five years
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t]
                      for k in range(K) for t in range(T))

# Constraints

# Initial stock constraints
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k]

# Capacity constraints
for k in range(K):
    for t in range(T):
        if t >= 2:
            capacity_constraint = data['capacity'][k] + pulp.lpSum(buildcapa[k][t-2] for k in range(K))
        else:
            capacity_constraint = data['capacity'][k]

        problem += produce[k][t] <= capacity_constraint

# Stock balance constraints
for k in range(K):
    for t in range(T):
        problem += stockhold[k][t+1] == stockhold[k][t] + produce[k][t] - pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) - data['demand'][k] - buildcapa[k][t]

# Solve the problem
problem.solve()

# Extract results
results = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T+1)] for k in range(K)]
}

print(results)

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')