import pulp
import json

# Data from the provided JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

K = len(data['inputone'])  # Number of industries
T = 5  # Planning horizon

# Initialize the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(1, T + 1)), "Total_Manpower"

# Constraints
for k in range(K):
    for t in range(1, T + 1):
        if t == 1:
            problem += (produce[k, t] + buildcapa[k, t] <= data['capacity'][k]), f"Initial_Capacity_Constraint_{k}_{t}"
        else:
            problem += (produce[k, t] + buildcapa[k, t] <= data['capacity'][k] + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t - 1] for j in range(K))), f"Capacity_Constraint_{k}_{t}"

for k in range(K):
    for t in range(1, T + 1):
        if t == 1:
            problem += (stockhold[k, t] == data['stock'][k] + pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) - data['demand'][k]), f"Stock_Constraint_{k}_{t}"
        else:
            problem += (stockhold[k, t] == data['stock'][k] + pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t - 1] for j in range(K)) - data['demand'][k]), f"Stock_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')