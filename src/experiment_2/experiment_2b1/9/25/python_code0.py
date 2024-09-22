import pulp
import numpy as np
import json

data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['stock'])  # Number of industries
T = 3  # Number of years to consider (0, 1, 2)

# Create variables for production, capacity building, and stock holding
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Problem definition
problem = pulp.LpProblem("Maximize_Total_Production", pulp.LpMaximize)

# Objective function: Maximize production in the last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(1, T)), "Total_Production"

# Constraints
# Manpower Constraint
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) +
                 pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K))) <= data['manpower_limit'], f"Manpower_Capacity_{t}"

# Production capacity constraints
for k in range(K):
    for t in range(T):
        if t > 0:
            problem += (produce[k][t] + stockhold[k][t-1] - stockhold[k][t] <= data['capacity'][k] + buildcapa[k][t-1]), f"Prod_Capacity_{k}_{t}"

# Linking current production to future capacities
for k in range(K):
    for t in range(T - 1):
        problem += (buildcapa[k][t] <= data['capacity'][k] - stockhold[k][t+1]), f"BuildCap_Limit_{k}_{t}"

# Initial conditions for stocks
for k in range(K):
    stockhold[k][0] = data['stock'][k]

# Solve the problem
problem.solve()

# Prepare results
result = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')