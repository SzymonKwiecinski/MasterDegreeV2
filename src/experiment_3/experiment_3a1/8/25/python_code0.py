import pulp
import numpy as np

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Parameters
K = len(data['stock'])  # Number of industries
T = 5  # Assume a time horizon of 5 years

# Create the LP problem
problem = pulp.LpProblem("Economic_Production_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T] for k in range(K)), "Total_Production"

# Constraints
# Production constraints
for k in range(K):
    for t in range(1, T):
        problem += stock[k, t-1] + produce[k, t] + pulp.lpSum(produce[j, t-1] * data['inputone'][k][j] for j in range(K)) >= 0, f"Production_Constraint_{k}_{t}"

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + \
               pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

# Capacity building constraints
for k in range(K):
    problem += data['capacity'][k] + pulp.lpSum(buildcapa[k, t] for t in range(T-2)) >= 0, f"Capacity_Building_Constraint_{k}"

# Stock balance constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += stock[k, t] == data['stock'][k] + produce[k, t] - pulp.lpSum(buildcapa[j, t] * data['inputtwo'][j][k] for j in range(K)), f"Stock_Balance_Constraint_{k}_{t}"
        else:
            problem += stock[k, t] == stock[k, t-1] + produce[k, t] - pulp.lpSum(buildcapa[j, t] * data['inputtwo'][j][k] for j in range(K)), f"Stock_Balance_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')