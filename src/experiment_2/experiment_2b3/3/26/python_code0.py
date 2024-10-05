import pulp

# Data
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

# Constants
K = len(data["capacity"])
T = 5

# Problem setup
problem = pulp.LpProblem("EconomicProduction", pulp.LpMaximize)

# Decision variables
produce = [[pulp.LpVariable(f"produce_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]
buildcapa = [[pulp.LpVariable(f"buildcapa_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]
stockhold = [[pulp.LpVariable(f"stockhold_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]

# Objective function: Maximize total manpower over 5 years
problem += pulp.lpSum(data["manpowerone"][k] * produce[k][t] + data["manpowertwo"][k] * buildcapa[k][t] for k in range(K) for t in range(T))

# Capacity and demand constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            # Year 0 capacity constraints
            problem += produce[k][t] <= data["capacity"][k] + data["stock"][k]
        else:
            # Subsequent years' capacity constraints
            problem += produce[k][t] <= pulp.lpSum(produce[k][t-1] * data["inputtwo"][k][j] for j in range(K)) + stockhold[k][t-1]
        if t > 0:
            # Demand constraints
            problem += produce[k][t] + stockhold[k][t] >= data["demand"][k]

# Input balance constraints
for t in range(T):
    for k in range(K):
        if t == 0:
            problem += produce[k][t] + buildcapa[k][t] + stockhold[k][t] == data["stock"][k]
        else:
            problem += produce[k][t] + buildcapa[k][t] + stockhold[k][t] == stockhold[k][t-1] + pulp.lpSum(produce[j][t-1] * data["inputone"][k][j] for j in range(K))

# Solve problem
problem.solve()

# Output results
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

print(f"Output: {output}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")