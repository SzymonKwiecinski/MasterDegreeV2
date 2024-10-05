import pulp

# Read data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['stock'])
T = 3  # Assuming a 3-year period for simplicity

# Initialize the problem
problem = pulp.LpProblem("Industry_Production_Optimization", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T-1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T-2] for k in range(K))

# Constraints

# Initial stock and capacity
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]
    problem += produce[k, 0] <= data['capacity'][k] + data['stock'][k]

# Production constraints
for k in range(K):
    for t in range(1, T):
        problem += produce[k, t] <= data['capacity'][k] + stockhold[k, t-1]

# Input constraints
for k in range(K):
    for t in range(1, T):
        problem += sum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + stockhold[k, t-1] >= produce[k, t]

# Manpower constraints
for t in range(T):
    problem += (sum(data['manpowerone'][k] * produce[k, t] for k in range(K)) +
                sum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K-1))) <= data['manpower_limit']

# Capacity building constraints
for k in range(K):
    for t in range(0, T-2):
        problem += (data['capacity'][k] +
                    sum(buildcapa[k, s] * data['inputtwo'][k][j] for j in range(K) for s in range(t+1))) >= produce[k, t+2]

# Stock holding constraints
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - 0  # "consume" is assumed to be zero

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')