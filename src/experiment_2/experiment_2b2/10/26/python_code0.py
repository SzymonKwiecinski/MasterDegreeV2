import pulp

# Input Data
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

K = len(manpowerone)
T = 5

# Create LP Problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective: Maximize total manpower requirement
problem += pulp.lpSum(produce[k, t] * manpowerone[k] + buildcapa[k, t] * manpowertwo[k] for k in range(K) for t in range(T))

# Constraints
for k in range(K):
    for t in range(T):
        # Capacity constraints
        if t == 0:
            problem += produce[k, t] <= capacity[k]
        else:
            prev_build_capa = sum(buildcapa[k, t_prev] for t_prev in range(max(0, t-2), t))
            problem += produce[k, t] <= capacity[k] + prev_build_capa

        # Stock balances
        if t == 0:
            problem += produce[k, t] + stock[k] == stockhold[k, t] + demand[k]
        else:
            problem += produce[k, t] + stockhold[k, t-1] == stockhold[k, t] + demand[k]

        # Input constraints
        for j in range(K):
            problem += pulp.lpSum(inputone[k][j] * produce[k, t] + inputtwo[k][j] * buildcapa[k, t] for k in range(K)) <= produce[j, t]

# Solve
problem.solve()

# Output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')