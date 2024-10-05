import pulp
import numpy as np

# Data from JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(1, T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + 
                      data['manpowertwo'][k] * buildcapa[k][t] 
                      for k in range(K) for t in range(1, T+1)), "Total_Manpower_Requirement"

# Capacity Constraints
for k in range(K):
    for t in range(1, T+1):
        if t == 1:
            problem += produce[k][t] <= data['capacity'][k], f"Capacity_Constraint_{k}_{t}"
        else:
            problem += produce[k][t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k][tau] for tau in range(1, t-1)), \
                        f"Capacity_Constraint_{k}_{t}"

# Stock Balance Constraints
for k in range(K):
    for t in range(1, T+1):
        if t == 1:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t] \
                        - pulp.lpSum(data['inputone'][j][k] * produce[j][t] for j in range(K)) \
                        - pulp.lpSum(data['inputtwo'][j][k] * buildcapa[j][t] for j in range(K)) \
                        - data['demand'][k], f"Stock_Balance_Constraint_{k}_{t}"
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] \
                        - pulp.lpSum(data['inputone'][j][k] * produce[j][t] for j in range(K)) \
                        - pulp.lpSum(data['inputtwo'][j][k] * buildcapa[j][t] for j in range(K)) \
                        - data['demand'][k], f"Stock_Balance_Constraint_{k}_{t}"

# Initial Stock Constraints
for k in range(K):
    problem += stockhold[k][1] == data['stock'][k], f"Initial_Stock_Constraint_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')