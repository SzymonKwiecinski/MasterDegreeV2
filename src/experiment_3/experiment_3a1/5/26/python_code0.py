import pulp
import json

# Given data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Constants
K = len(data['inputone'])
T = 5

# Create the linear programming problem
problem = pulp.LpProblem("Industry_Production_Capacity_Building", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K) for t in range(T)) + \
           pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(T))

# Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= data['capacity'][k] + (stockhold[k, t-1] if t > 0 else data['stock'][k]), f"Production_Capacity_Constraint_{k}_{t}"
        problem += produce[k, t] >= data['demand'][k], f"Demand_Constraint_{k}_{t}"

# Input Requirements
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) + (stockhold[k, t-1] if t > 0 else 0) >= produce[k, t], f"Input_Requirement_Constraint_{k}_{t}"

# Capacity Building Constraints
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) <= data['manpowerone'][k] * buildcapa[k, t], f"Capacity_Building_Constraint_{k}_{t}"

# Stockholding Constraints
for k in range(K):
    for t in range(T):
        problem += stockhold[k, t] == (stockhold[k, t-1] if t > 0 else data['stock'][k]) + produce[k, t] - data['demand'][k], f"Stockholding_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')