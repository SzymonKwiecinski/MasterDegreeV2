import pulp
import json

# Data from the provided JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Define parameters
K = len(data['stock'])
T = 3  # Assuming T-1 and T to be 2 and 3.

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Define decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", (range(K), range(T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum([produce[k][t] for k in range(K) for t in range(T-1, T)])

# Constraints
# Initial stocks and capacities
for k in range(K):
    stock[k][0] = data['stock'][k]
    
# Production and Stock Constraints
for k in range(K):
    for t in range(T):
        if t < T - 1:
            problem += produce[k][t] + buildcapa[k][t] + stock[k][t+1] == data['capacity'][k] + stock[k][t]

# Capacity constraints
for k in range(K):
    for t in range(1, T):
        problem += stock[k][t] == data['capacity'][k] + buildcapa[k][t-1]

# Input Constraints
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) <= data['capacity'][k]
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K)) <= data['capacity'][k]

# Manpower Constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t]
                          for k in range(K)) <= data['manpower_limit']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')