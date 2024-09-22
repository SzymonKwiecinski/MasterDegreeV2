import pulp
import json

# Load the data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Data extraction
inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
manpower_limit = data['manpower_limit']

K = len(inputone)
T = 5  # Assuming a planning horizon of 5 years (0 to 4)

# Create the problem
problem = pulp.LpProblem("Economic_Capacity_and_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([produce[k, T - 1] + produce[k, T] for k in range(K)])

# Production Constraints
for k in range(K):
    for t in range(1, T):
        problem += produce[k, t] <= capacity[k] + stockhold[k, t - 1], f"Prod_Constraint_{k}_{t}"

# Input Requirements
for k in range(K):
    for t in range(1, T):
        problem += pulp.lpSum([inputone[k][j] * produce[j, t - 1] for j in range(K)]) + stockhold[k, t - 1] >= produce[k, t], f"Input_Requirement_{k}_{t}"

# Manpower Constraints
for t in range(1, T):
    problem += pulp.lpSum([manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K)]) <= manpower_limit, f"Manpower_Constraint_{t}"

# Capacity Building
for k in range(K):
    for t in range(T - 2):
        problem += capacity[k] + pulp.lpSum([inputtwo[k][j] * buildcapa[j, t] for j in range(K)]) >= capacity[k] + t + 2, f"Capacity_Building_{k}_{t}"

# Stock Dynamics
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k, t] == stock[k] + stockhold[k, t - 1] + produce[k, t - 1] - produce[k, t], f"Stock_Dynamics_{k}_{t}"

# Solve the problem
problem.solve()

# Output the results
for k in range(K):
    for t in range(1, T):
        print(f'produce[{k},{t}]: {produce[k, t].varValue}')
        print(f'buildcapa[{k},{t}]: {buildcapa[k, t].varValue}')
        print(f'stockhold[{k},{t}]: {stockhold[k, t].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')