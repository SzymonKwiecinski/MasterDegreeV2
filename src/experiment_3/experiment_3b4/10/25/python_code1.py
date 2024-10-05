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

K = len(data['stock'])
T = 2  # Time periods

# Initialize LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
capacity = pulp.LpVariable.dicts("capacity", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, T - 1] for k in range(K))

# Constraints
# Initial Stock and Capacity
for k in range(K):
    problem += (stockhold[k, 0] == data['stock'][k])
    problem += (capacity[k, 0] == data['capacity'][k])

# Production Capacity
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (produce[k, t] <= capacity[k, t] + stockhold[k, t])
        else:
            problem += (produce[k, t] <= capacity[k, t - 1] + stockhold[k, t - 1])

# Manpower Constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'])

# Input Balance for Production and Capacity Building
for k in range(K):
    for t in range(1, T):  # Start from 1 to avoid negative indexing
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j, t] + data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) <= (stockhold[k, t - 1] + produce[k, t - 1]))

# Stock Flow Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (stockhold[k, t] == data['stock'][k] + produce[k, t] - pulp.lpSum(data['inputone'][j][k] * produce[j, t] + data['inputtwo'][j][k] * buildcapa[j, t] for j in range(K)))
        else:
            problem += (stockhold[k, t] == stockhold[k, t - 1] + produce[k, t] - pulp.lpSum(data['inputone'][j][k] * produce[j, t] + data['inputtwo'][j][k] * buildcapa[j, t] for j in range(K)))

# Capacity Increase Constraints
for k in range(K):
    for t in range(1, T):  # Corrected to avoid t out of bounds
        problem += (capacity[k, t] == capacity[k, t - 1] + buildcapa[k, t - 1])

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')