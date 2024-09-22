import pulp
import json

# Load the data from JSON format
data = '''{
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    "manpowerone": [0.6, 0.3, 0.2], 
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    "manpowertwo": [0.4, 0.2, 0.1], 
    "stock": [150, 80, 100], 
    "capacity": [300, 350, 280], 
    "manpower_limit": 470000000.0
}'''
data = json.loads(data)

# Parameters
K = len(data['inputone'])
T = 2  # Considering two years: T-1 and T

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T+1)), lowBound=0)
capacity = pulp.LpVariable.dicts("capacity", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum([produce[k][T-1] + produce[k][T] for k in range(K)])

# Constraints

# Production Constraints
for k in range(K):
    for t in range(T+1):
        problem += produce[k][t] <= capacity[k], f"Production_Constraint_{k}_{t}"

# Resource Constraints
for k in range(K):
    for t in range(T+1):
        problem += pulp.lpSum([data['inputone'][k][j] * produce[k][t] + data['inputtwo'][k][j] * buildcapa[k][t] for j in range(K)]) <= stockhold[k][t] + produce[k][t], f"Resource_Constraint_{k}_{t}"

# Manpower Constraints
for t in range(T+1):
    problem += pulp.lpSum([data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)]) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

# Stock Balance Constraints
for k in range(K):
    for t in range(T):
        problem += stockhold[k][t+1] == stockhold[k][t] + produce[k][t] - pulp.lpSum([data['inputone'][j][k] * produce[j][t] for j in range(K)]) - buildcapa[k][t], f"Stock_Balance_Constraint_{k}_{t}"

# Capacity Update Constraints
for k in range(K):
    for t in range(T):
        problem += capacity[k] == capacity[k] + buildcapa[k][t], f"Capacity_Update_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')