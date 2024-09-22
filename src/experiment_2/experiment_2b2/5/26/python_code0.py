import pulp

# Data input
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

inputone = data["inputone"]
manpowerone = data["manpowerone"]
inputtwo = data["inputtwo"]
manpowertwo = data["manpowertwo"]
stock = data["stock"]
capacity = data["capacity"]
demand = data["demand"]

K = len(capacity)
T = 5

# Define the LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = [[pulp.LpVariable(f"produce_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]
buildcapa = [[pulp.LpVariable(f"buildcapa_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]
stockhold = [[pulp.LpVariable(f"stockhold_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]

# Objective: Maximize total manpower requirement over five years
problem += pulp.lpSum([
    pulp.lpSum([manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K)])
    for t in range(T)
])

# Constraints
for t in range(T):
    for k in range(K):
        # Demand Satisfaction Constraint
        if t >= 1:
            problem += (produce[k][t] + stockhold[k][t-1] == demand[k] + stockhold[k][t] + 
                        pulp.lpSum([inputone[k][j] * produce[j][t] for j in range(K)]) + 
                        pulp.lpSum([inputtwo[k][j] * buildcapa[j][t] for j in range(K)]))
        else:
            problem += (produce[k][t] + stock[k] == demand[k] + stockhold[k][t] + 
                        pulp.lpSum([inputone[k][j] * produce[j][t] for j in range(K)]) + 
                        pulp.lpSum([inputtwo[k][j] * buildcapa[j][t] for j in range(K)]))
        
        # Capacity Constraint
        if t == 0:
            problem += produce[k][t] <= capacity[k]
        elif t == 1:
            problem += produce[k][t] <= capacity[k] + buildcapa[k][t-1]
        else:
            problem += produce[k][t] <= capacity[k] + buildcapa[k][t-1] + buildcapa[k][t-2]

# Solve the problem
problem.solve()

# Extract results
results = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')