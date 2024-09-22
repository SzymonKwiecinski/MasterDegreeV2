import pulp
import json

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
T = 2  # Considering T = 2 for the last two years

# Define the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Define variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T+1)), lowBound=0)
capacity = pulp.LpVariable.dicts("capacity", (range(K), range(T+1)), lowBound=0)

# Initial conditions
for k in range(K):
    stockhold[k][0] = data['stock'][k]
    capacity[k][0] = data['capacity'][k]

# Objective function
objective = pulp.lpSum(produce[k][T-1] + produce[k][T] for k in range(K))
problem += objective

# Constraints
# Production Constraints
for k in range(K):
    for t in range(T+1):
        problem += produce[k][t] <= capacity[k][t]

# Manpower Constraints
for t in range(T+1):
    problem += pulp.lpSum(
        data['manpowerone'][k] * produce[k][t] +
        data['manpowertwo'][k] * buildcapa[k][t]
        for k in range(K)
    ) <= data['manpower_limit']

# Input Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) +
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K))
            <= stockhold[k][t-1] + produce[k][t]
        )

# Stock Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += (
            stockhold[k][t] == stockhold[k][t-1] + produce[k][t] -
            pulp.lpSum(data['inputone'][j][k] * produce[j][t] for j in range(K))
        )

# Capacity Update
for k in range(K):
    for t in range(T-1):
        problem += (capacity[k][t+2] == capacity[k][t+1] + buildcapa[k][t])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')