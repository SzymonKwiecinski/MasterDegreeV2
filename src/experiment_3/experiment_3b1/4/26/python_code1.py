import pulp
import json

# Data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

K = len(data['manpowerone'])
T = 5

# Problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stock", (range(K), range(T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K) for t in range(1, T + 1)) + \
           pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K) for t in range(1, T + 1))

# Constraints
# Production capacity constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k][t] <= stockhold[k][t - 1] + data['capacity'][k] + \
                   pulp.lpSum(data['inputone'][j][k] * produce[j][t - 1] for j in range(K))

# Demand satisfaction constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k][t] + stockhold[k][t - 1] - stockhold[k][t] >= data['demand'][k]

# Capacity building constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += buildcapa[k][t] <= stockhold[k][t - 1] + \
                   pulp.lpSum(data['inputtwo'][j][k] * produce[j][t - 1] for j in range(K))

# Manpower constraints
available_manpower = 1000  # Assuming an arbitrary available manpower for this example
for k in range(K):
    for t in range(1, T + 1):
        problem += data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] <= available_manpower

# Stock balance constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += stockhold[k][t] == stockhold[k][t - 1] + produce[k][t] - data['demand'][k] + buildcapa[k][t]

# Initial conditions
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k]
    problem += produce[k][0] == 0
    problem += buildcapa[k][0] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')