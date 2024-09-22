import pulp
import json

# Data in JSON format
data_json = """{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}"""
data = json.loads(data_json)

K = len(data['demand'])  # Number of industries
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Economic_Production_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)] for k in range(K) for t in range(1, T+1))

# Constraints
# Initial Stock
for k in range(K):
    problem += stockhold[(k, 0)] == data['stock'][k]

# Production Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[(k, t)] <= data['capacity'][k] + stockhold[(k, t-1)]

# Demand Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[(k, t)] + stockhold[(k, t-1)] >= data['demand'][k]

# Stock Balance Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += stockhold[(k, t)] == stockhold[(k, t-1)] + produce[(k, t-1)] - data['demand'][k]

# Capacity Building Constraints
for k in range(K):
    problem += data['capacity'][k] + pulp.lpSum(buildcapa[(k, t)] for t in range(1, T+1)) >= 0

# Input Requirements for Production
for t in range(1, T+1):
    for k in range(K):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[(j, t)] for j in range(K)) >= 0

# Input Requirements for Capacity Building
for t in range(1, T+1):
    for k in range(K):
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[(j, t)] for j in range(K)) >= 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')