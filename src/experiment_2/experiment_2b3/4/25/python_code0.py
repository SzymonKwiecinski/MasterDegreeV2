import pulp

# Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['capacity'])
T = 5

# Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T-2, T))

# Constraints
for k in range(K):
    # Initial stock constraint
    problem += stockhold[k, 0] == data['stock'][k]

    for t in range(T):
        # Capacity constraints
        if t == 0:
            problem += produce[k, t] <= data['capacity'][k]
        else:
            problem += produce[k, t] <= data['capacity'][k] + buildcapa[k, t-2] if t >= 2 else data['capacity'][k]

        # Stock constraint
        problem += produce[k, t] + stockhold[k, t] == stockhold[k, t+1] if t < T-1 else stockhold[k, t]

        # Manpower constraints
        problem += (pulp.lpSum(data['manpowerone'][j] * produce[j, t] for j in range(K)) + 
                    pulp.lpSum(data['manpowertwo'][j] * buildcapa[j, t] for j in range(K)) <= data['manpower_limit'])

        # Input constraints
        for j in range(K):
            if t > 0:
                problem += (pulp.lpSum(data['inputone'][k][j] * produce[k, t] for k in range(K)) +
                            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[k, t] for k in range(K))) <= produce[j, t-1] + stockhold[j, t-1]

# Solve
problem.solve()

# Output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")