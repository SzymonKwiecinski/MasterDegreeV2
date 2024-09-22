import pulp
import numpy as np

# Data
data = {
    'inputone': np.array([[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]]),
    'manpowerone': np.array([0.6, 0.3, 0.2]),
    'inputtwo': np.array([[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]]),
    'manpowertwo': np.array([0.4, 0.2, 0.1]),
    'stock': np.array([150, 80, 100]),
    'capacity': np.array([300, 350, 280]),
    'demand': np.array([60000000.0, 60000000.0, 30000000.0])
}

K = len(data['manpowerone'])
T = 5

# Create the problem
problem = pulp.LpProblem("Economic_Production_and_Capacity_Building", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
                       for k in range(K) for t in range(1, T + 1))

# Production Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k, t] <= data['capacity'][k] + (stockhold[k, t - 1] if t > 1 else data['stock'][k])

# Input Requirement Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k, t] >= pulp.lpSum(data['inputone'][k, j] * produce[j, t - 1] for j in range(K)) + data['demand'][k]

# Stock Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += stockhold[k, t] == data['stock'][k] + (stockhold[k, t - 1] if t > 1 else 0) + produce[k, t] - data['demand'][k]

# Capacity Building Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += data['capacity'][k] + pulp.lpSum(data['inputtwo'][k, j] * buildcapa[j, t - 1] for j in range(K)) >= 0  # This is just to ensure that capacity can build

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')