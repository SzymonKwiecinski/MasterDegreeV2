import pulp
import json

# Load data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

K = len(data['inputone'])  # number of industries
T = 3  # number of years (0, 1, 2)

# Create the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T-1, T))

# Constraints

# Production and Capacity Constraints
for k in range(K):
    for t in range(1, T):
        problem += produce[k][t] + buildcapa[k][t] <= data['capacity'][k] + stockhold[k][t-1]

# Input Constraints
for k in range(K):
    for t in range(1, T):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[k][t] for j in range(K)) <= data['inputone'][k][t-1]

# Manpower Constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit']

# Stock Constraints
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - pulp.lpSum(data['inputone'][k][j] * produce[k][t] for j in range(K))

# Initial Conditions
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k]
    problem += buildcapa[k][0] == data['capacity'][k]

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')