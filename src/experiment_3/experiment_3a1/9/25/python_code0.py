import pulp
import json

# Data from JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])  # Number of industries
T = 5  # Assuming a planning horizon of 5 years

# Create a linear programming problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, T] + produce[k, T - 1] for k in range(K)), "Total_Production"

# Capacity constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[j, t - 2] for j in range(K) if t > 2), f"Capacity_Constraint_{k}_{t}"

# Stock constraints
for k in range(K):
    for t in range(1, T + 1):
        if t == 1:
            problem += stock[k, t] == data['stock'][k] + produce[k, t - 1], f"Stock_Constraint_{k}_{t}"
        else:
            problem += stock[k, t] == stock[k, t - 1] + produce[k, t - 1] - pulp.lpSum(data['inputone'][j][k] * produce[j, t - 1] for j in range(K)), f"Stock_Constraint_{k}_{t}"

# Non-negativity constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += stock[k, t] >= 0, f"Non_Negative_Stock_{k}_{t}"

# Manpower constraints
for t in range(1, T + 1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

# Production constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k, t] >= 0, f"Non_Negative_Produce_{k}_{t}"
        problem += buildcapa[k, t] >= 0, f"Non_Negative_BuildCapa_{k}_{t}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')