import pulp
import json

# Data input
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

K = len(data['manpowerone'])
T = 5

# Create a problem variable
problem = pulp.LpProblem("Economic_Industries_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(0, T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] for k in range(K) for t in range(1, T + 1)) + \
           pulp.lpSum(data['manpowertwo'][k] * buildcapa[(k, t)] for k in range(K) for t in range(1, T + 1))

# Constraints

# Capacity Constraints
for k in range(K):
    for t in range(1, T + 1):
        if t == 1:
            problem += produce[(k, t)] + (data['stock'][k] if t == 1 else stockhold[(k, t-1)]) == data['capacity'][k] + stockhold[(k, t)]
        else:
            problem += produce[(k, t)] + stockhold[(k, t - 1)] == data['capacity'][k] + stockhold[(k, t)]

# Input Constraints for Production
for k in range(K):
    for t in range(1, T + 1):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[(j, t - 1)] for j in range(K)) + data['stock'][k] >= produce[(k, t)]

# Input Constraints for Capacity Building
for k in range(K):
    for t in range(1, T + 1):
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[(j, t)] for j in range(K)) + data['manpowerone'][k] * produce[(k, t)] <= data['capacity'][k] + stockhold[(k, t)]

# Demand Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[(k, t)] + (data['stock'][k] if t == 1 else stockhold[(k, t - 1)]) >= data['demand'][k]

# Initial Stock and Capacity
for k in range(K):
    problem += stockhold[(k, 0)] == data['stock'][k]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')