import pulp
import json

# Load the data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Parameters
K = len(data['inputone'])  # Number of industries
T = 2  # Number of years considered for production

# Initialize the problem
problem = pulp.LpProblem("Industry_Production_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, T] + produce[k, T - 1] for k in range(K))

# Constraints
# Production Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k, t] <= data['capacity'][k] + (stockhold[k, t-1] if t > 1 else data['stock'][k])

# Input Requirements for Production
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k, t] <= pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + (stockhold[k, t-1] if t > 1 else data['stock'][k])

# Manpower Constraints for Production
for t in range(1, T + 1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) <= data['manpower_limit']

# Constraints for Building Capacity
for k in range(K):
    for t in range(1, T + 1):
        problem += buildcapa[k, t] <= data['capacity'][k] + (stockhold[k, t-1] if t > 1 else data['stock'][k])

# Input Requirements for Building Capacity
for k in range(K):
    for t in range(1, T + 1):
        problem += buildcapa[k, t] <= pulp.lpSum(data['inputtwo'][k][j] * produce[j, t-1] for j in range(K)) + (stockhold[k, t-1] if t > 1 else data['stock'][k])

# Manpower Constraints for Building Capacity
for t in range(1, T + 1):
    problem += pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']

# Stock Holding Update
for k in range(K):
    for t in range(1, T + 1):
        problem += stockhold[k, t] == data['stock'][k] + (stockhold[k, t-1] if t > 1 else data['stock'][k]) + produce[k, t] - buildcapa[k, t]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')