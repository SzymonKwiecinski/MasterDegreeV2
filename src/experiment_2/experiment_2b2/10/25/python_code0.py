import pulp

# Input data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Initialize decision variables based on problem structure
K = len(data['inputone'])  # Number of industries
T = 5                      # Planning period

# Decision variables: Produce, Build Capacity, Stockhold
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Set the objective: Maximize production in the last two years
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in [T-2, T-1])

# Initial stock and capacity constraints
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]
    problem += produce[k, 0] <= data['capacity'][k]

# Stock balance constraints
for k in range(K):
    for t in range(1, T):
        problem += (
            produce[k, t] + stockhold[k, t-1]
            - pulp.lpSum(data['inputone'][i][k] * produce[i, t] for i in range(K))
            - pulp.lpSum(data['inputtwo'][i][k] * buildcapa[i, t] for i in range(K))
            == stockhold[k, t]
        )

# Capacity constraints
for k in range(K):
    for t in range(1, T):
        if t >= 2:
            problem += (
                produce[k, t]
                <= data['capacity'][k]
                + pulp.lpSum(buildcapa[k, t-2-t1] for t1 in range(t-1))
            )

# Manpower constraints
for t in range(T):
    problem += (
        pulp.lpSum(data['manpowerone'][k] * produce[k, t]
                   + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K))
        <= data['manpower_limit']
    )

# Solve the problem
problem.solve()

# Collect results for OUTPUT FORMAT
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')