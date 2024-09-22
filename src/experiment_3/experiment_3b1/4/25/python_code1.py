import pulp
import json

# Load data from JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Define the model
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Parameters
K = len(data['stock'])
T = 3  # Assume we are modeling for 3 years

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
capacity = pulp.LpVariable.dicts("capacity", (k for k in range(K)), lowBound=0)

# Set the objective function
problem += pulp.lpSum(produce[k, T-1] for k in range(K))

# Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= capacity[k] + (stockhold[k, t-1] if t > 0 else data['stock'][k])

# Input Constraints
for k in range(K):
    for t in range(1, T):  # Start from year 1
        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) +
            (pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-2] for j in range(K)) if t > 1 else 0) + 
            stockhold[k, t-1] >= produce[k, t]
        )

# Manpower Constraints
for t in range(T):
    problem += (
        pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + 
        pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']
    )

# Building Capacity Constraints
for k in range(K):
    for t in range(T - 2):  # We need t and t+2
        problem += capacity[k] == (data['capacity'][k] + pulp.lpSum(buildcapa[j, t] for j in range(K)))

# Stock Constraints
for k in range(K):
    for t in range(1, T):
        problem += (
            stockhold[k, t] == stockhold[k, t-1] + produce[k, t-1] - 
            pulp.lpSum(data['inputone'][j][k] * produce[j, t] for j in range(K))
        )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')