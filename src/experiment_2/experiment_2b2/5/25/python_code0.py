import pulp

# Data from JSON input
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "manpower_limit": 470000000.0
}

inputone = data["inputone"]
manpowerone = data["manpowerone"]
inputtwo = data["inputtwo"]
manpowertwo = data["manpowertwo"]
stock = data["stock"]
capacity = data["capacity"]
manpower_limit = data["manpower_limit"]

K = len(inputone)  # number of industries
T = 5  # planning for 5 years

# Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')

# Objective function: Maximize total production in the last two years (years 4 and 5)
problem += pulp.lpSum([produce[k, t] for k in range(K) for t in range(T-2, T)])

# Constraints
for t in range(T):
    for k in range(K):
        # Capacity constraint
        if t == 0:
            problem += produce[k, t] <= capacity[k]

        else:
            problem += produce[k, t] <= produce[k, t-1] + buildcapa[k, t-2] if t >= 2 else produce[k, t-1] + capacity[k]

        # Stock balance constraint
        if t == 0:
            problem += stockhold[k, t] == stock[k] - produce[k, t] - buildcapa[k, t]
        else:
            problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - buildcapa[k, t]

        # Input constraints
        for j in range(K):
            problem += produce[k, t] + buildcapa[k, t] <= stockhold[j, t] / inputone[k][j]

    # Manpower constraint
    problem += pulp.lpSum(produce[k, t] * manpowerone[k] + buildcapa[k, t] * manpowertwo[k] for k in range(K)) <= manpower_limit

# Solve
problem.solve()

# Extract results
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T+1)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')