import pulp
import json

# Load data from JSON
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Create the LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

K = len(data['manpowerone'])  # Number of industries
T = 5  # Time periods

# Define decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K) for t in range(1, T + 1)) + \
           pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(1, T + 1)), "Total Manpower Requirement"

# Constraints
# Initial stock
for k in range(K):
    problem += stock[k, 0] == data['stock'][k], f"InitialStock_k{k}"

# Production constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += (produce[k, t] + stock[k, t - 1] - stock[k, t] ==
                     pulp.lpSum(data['inputone'][k][j] * produce[j, t - 1] for j in range(K)) + stock[k, t - 1]), f"ProductionConstraint_k{k}_t{t}"

# Capacity building constraints
for k in range(K):
    problem += (data['capacity'][k] + pulp.lpSum(buildcapa[k, t] for t in range(1, T + 1)) <=
                 data['capacity'][k] + 2 * pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t - 1] for j in range(K) for t in range(1, T + 1))), f"CapacityBuildingConstraint_k{k}"

# Demand constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += (produce[k, t] + stock[k, t - 1] - stock[k, t] >= data['demand'][k]), f"DemandConstraint_k{k}_t{t}"

# Stock constraints (already covered in the variable definition with lowBound=0)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')