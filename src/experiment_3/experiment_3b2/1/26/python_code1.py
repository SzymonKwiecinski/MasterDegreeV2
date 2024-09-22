import pulp
import json

# Load data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Parameters
K = len(data['capacity'])
T = 5

# Create a problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T + 1)), lowBound=0)

# Initial stock
for k in range(K):
    stockhold[(k, 0)] = data['stock'][k]

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)] for k in range(K) for t in range(1, T + 1))

# Constraints
# Capacity Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[(k, t)] <= data['capacity'][k] + pulp.lpSum(buildcapa[(k, tau)] for tau in range(1, t))

# Demand Satisfaction
for k in range(K):
    for t in range(1, T + 1):
        problem += (produce[(k, t)] + stockhold[(k, t - 1)] >= 
                     data['demand'][k] + pulp.lpSum(data['inputone'][k][j] * produce[(j, t)] for j in range(K)) + 
                     pulp.lpSum(data['inputtwo'][k][j] * buildcapa[(j, t)] for j in range(K)) + 
                     stockhold[(k, t)])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')