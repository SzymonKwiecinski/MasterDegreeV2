import pulp
import json

# Data from JSON
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Constants
K = len(data['manpowerone'])
T = 5

# Problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(T))

# Constraints
# Stock Balance
for k in range(K):
    for t in range(T):
        problem += (stockhold[k, t-1] + produce[k, t] - pulp.lpSum(data['inputone'][j][k] * produce[j, t] for j in range(K)) - data['demand'][k] == stockhold[k, t])

# Production Capacity
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= (data['capacity'][k] + pulp.lpSum(buildcapa[k, tau] for tau in range(max(0, t-1))))

# Resource Constraints for Building Capacity
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(data['inputtwo'][j][k] * buildcapa[k, t] for j in range(K)) <= pulp.lpSum(produce[j, tau] for tau in range(t+1) for j in range(K))

# Initial Conditions
for k in range(K):
    problem += stockhold[k, -1] == data['stock'][k]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')