import pulp
import numpy as np

# Data from JSON
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
T = 2  # Assuming we are considering 2 years (T=1 for year 1 and T=2 for year 2)

# Initialize the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, T] + produce[k, T - 1] for k in range(K))

# Constraints
# Initial Conditions
for k in range(K):
    stockhold[k, 0] = data['stock'][k]
    capacity_k = data['capacity'][k]

# Production constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += produce[k, t] <= capacity_k + stockhold[k, t - 1]

# Input requirement for production
for t in range(1, T + 1):
    for k in range(K):
        problem += produce[k, t] <= pulp.lpSum(data['inputone'][k][j] * produce[j, t - 1] for j in range(K)) + stockhold[k, t - 1]

# Manpower constraint for production
for t in range(1, T + 1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) <= data['manpower_limit']

# Capacity building
for t in range(1, T + 1):
    for k in range(K):
        problem += buildcapa[k, t] <= capacity_k + stockhold[k, t - 1]

# Input requirement for capacity building
for t in range(1, T + 1):
    for k in range(K):
        problem += buildcapa[k, t] <= pulp.lpSum(data['inputtwo'][k][j] * produce[j, t - 1] for j in range(K)) + stockhold[k, t - 1]

# Manpower constraint for capacity building
for t in range(1, T + 1):
    problem += pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']

# Stock update constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += stockhold[k, t] == stockhold[k, t - 1] + produce[k, t - 1]  # Assuming consume[k, t] is not modeled

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')