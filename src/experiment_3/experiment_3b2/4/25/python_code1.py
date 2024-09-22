import pulp
import json

# Load data from the provided JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Define indices
K = len(data['stock'])  # Number of industries
T = 3  # Number of time periods, which we assume is fixed for this example

# Create the problem variable
problem = pulp.LpProblem("Economic_Industries_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)
capacity = pulp.LpVariable.dicts("capacity", (range(K), range(T)), lowBound=0)  # Added capacity definition

# Objective function
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T))  # Fixed the objective function index

# Constraints

# Initial conditions
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k]
    problem += capacity[k][0] == data['capacity'][k]

# Production Capacity Constraint
for k in range(K):
    for t in range(T):
        problem += produce[k][t] <= data['capacity'][k]

# Input Requirement Constraint
for k in range(K):
    for t in range(1, T):
        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) +
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K)) 
            <= stockhold[k][t-1] + produce[k][t]
        )

# Manpower Constraint
for t in range(T):
    problem += (
        pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K))
        <= data['manpower_limit']
    )

# Stock Update Constraint
for k in range(K):
    for t in range(1, T):
        problem += (
            stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - 
            pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) -
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K))
        )

# Capacity Growth
for k in range(K):
    for t in range(T-2):
        problem += capacity[k][t+2] == capacity[k][t] + buildcapa[k][t]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')