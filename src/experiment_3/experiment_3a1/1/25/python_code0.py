import pulp
import numpy as np
import json

# Given data
data_json = """
{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
 'manpowerone': [0.6, 0.3, 0.2], 
 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
 'manpowertwo': [0.4, 0.2, 0.1], 
 'stock': [150, 80, 100], 
 'capacity': [300, 350, 280], 
 'manpower_limit': 470000000.0}
"""
data = json.loads(data_json.replace("'", "\""))

K = len(data['capacity'])
T = 5  # assuming T is 5 for a 5 year horizon

# Create the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Create decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum([produce[k, T-1] + produce[k, T] for k in range(K)]), "Total_Production"

# Adding Constraints

# Production Constraints
for k in range(K):
    for t in range(1, T):
        problem += produce[k, t] <= data['capacity'][k] + stock[k, t-1], f"Prod_Constraint_{k}_{t}"

# Input Constraints
for k in range(K):
    for t in range(1, T):
        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) +
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-1] for j in range(K)) <=
            data['capacity'][k] + stock[k, t-1],
            f"Input_Constraint_{k}_{t}"
        )

# Manpower Constraints
for t in range(1, T):
    problem += (
        pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) +
        pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <=
        data['manpower_limit'],
        f"Manpower_Constraint_{t}"
    )

# Stock Balance Constraints
for k in range(K):
    for t in range(1, T):
        problem += stock[k, t] == stock[k, t-1] + produce[k, t-1] - pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K)), f"Stock_Balance_{k}_{t}"

# Capacity Building Constraints
for k in range(K):
    for t in range(T - 2):
        problem += data['capacity'][k] + buildcapa[k, t] >= data['capacity'][k] + buildcapa[k, t], f"Capacity_Building_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')