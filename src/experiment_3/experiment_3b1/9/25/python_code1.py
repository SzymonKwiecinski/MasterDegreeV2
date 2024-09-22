import pulp
import json

# Data in JSON format
data_json = '''{
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "manpower_limit": 470000000.0
}'''

# Load data from JSON
data = json.loads(data_json)

# Model parameters
K = len(data['capacity'])  # Number of industries
T = 2                       # Last two years for production

# Create the problem
problem = pulp.LpProblem("Industrial_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T)), "Objective"

# Constraints
# 1. Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k][t] <= data['capacity'][k] + stockhold[k][t - 1], f"Prod_Constraint_{k}_{t}"

# 2. Input Constraints
for k in range(K):
    for t in range(1, T):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j][t - 1] for j in range(K)) +
                     pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t - 2] for j in range(K)) +
                     stockhold[k][t - 1] >= produce[k][t]), f"Input_Constraint_{k}_{t}"

# 3. Manpower Constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) +
                 pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit'], 
                 f"Manpower_Constraint_{t}")

# 4. Capacity Building Constraints
for k in range(K):
    for t in range(T):
        problem += buildcapa[k][t] >= 0, f"Capacity_Constraint_{k}_{t}"

# 5. Stockholding Constraints
for k in range(K):
    for t in range(T):
        problem += stockhold[k][t] >= 0, f"Stockhold_Constraint_{k}_{t}"

# 6. Initial conditions for stocks
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k], f"Initial_Stock_{k}"

# 7. Inventory for next year
for k in range(K):
    for t in range(1, T + 1):
        problem += stockhold[k][t] == (stockhold[k][t - 1] + produce[k][t - 1] - produce[k][t] + buildcapa[k][t - 1]), f"Inventory_Year_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')