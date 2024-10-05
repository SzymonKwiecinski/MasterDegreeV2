import pulp
import json

# Load data from JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Define the problem
problem = pulp.LpProblem("Economic_Planning", pulp.LpMaximize)

# Define parameters
K = len(data['manpowerone'])       # Number of products
T = 5                               # Time periods

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(
    produce[(k, t)] * data['manpowerone'][k] + 
    buildcapa[(k, t)] * data['manpowertwo'][k]
    for k in range(K) for t in range(1, T + 1)
)

# Constraints
# Capacity Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (produce[(k, t)] <= 
                     data['capacity'][k] + 
                     pulp.lpSum(buildcapa[(j, t - 2)] * data['inputtwo'][j][k] for j in range(K) if t > 2))

# Resource Balance Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (pulp.lpSum(produce[(j, t)] * data['inputone'][j][k] for j in range(K)) + 
                     pulp.lpSum(buildcapa[(j, t)] * data['inputtwo'][j][k] for j in range(K)) <= 
                     produce[(k, t)] + stockhold[(k, t)])

# Stock Update
for k in range(K):
    for t in range(2, T + 1):
        problem += (stockhold[(k, t)] == 
                     stockhold[(k, t - 1)] + 
                     produce[(k, t)] - data['demand'][k])

# Set initial stock for t=1
for k in range(K):
    problem += (stockhold[(k, 1)] == data['stock'][k])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')