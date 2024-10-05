import pulp

# Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0,
}

# Parameters
K = len(data['capacity'])  # Number of industries
T = 4  # Number of years we are considering

# Initialize the model
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective: Maximize production in the last two years
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T-2, T))

# Constraints
for k in range(K):
    # Initial stock constraints
    problem += stockhold[k, 0] == data['stock'][k]
    # Initial capacity constraints
    problem += produce[k, 0] <= data['capacity'][k]

    for t in range(1, T):
        # Stock-flow constraints
        problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t-1] - sum(data['inputone'][k][j] * produce[j, t] for j in range(K)) - buildcapa[k, t]
        
        # Capacity constraints
        if t < T - 1:
            problem += produce[k, t] <= data['capacity'][k] + buildcapa[k, t]
        else:
            problem += produce[k, t] <= data['capacity'][k] + sum(buildcapa[k, t-2] for t_2 in range(t-2+1))

    # Ensure positive production fits within manpower constraints each year
    for t in range(T):
        problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')