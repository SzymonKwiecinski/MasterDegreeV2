import pulp
import json

# Input Data in JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(0, T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K) for t in range(1, T+1))

# Constraints

# Stock Constraints
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k], f"Stock_Constraint_{k}"

# Production Constraints
for k in range(K):
    for t in range(1, T+1):
        if t == 1:
            problem += produce[k][t] + stockhold[k][t-1] == pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) + data['demand'][k] + stockhold[k][t], f"Production_Constraint_{k}_{t}"
        else:
            problem += produce[k][t] + stockhold[k][t-1] == pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) + data['demand'][k] + stockhold[k][t], f"Production_Constraint_{k}_{t}"

# Capacity Constraints
for k in range(K):
    for t in range(3, T+1):
        problem += produce[k][t] <= data['capacity'][k] + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-2] for j in range(K)), f"Capacity_Constraint_{k}_{t}"

# Demand Fulfillment Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k][t] >= data['demand'][k], f"Demand_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')