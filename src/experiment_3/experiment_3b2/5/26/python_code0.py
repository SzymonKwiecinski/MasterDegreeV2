import pulp
import numpy as np

# Data
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

# Create the model
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(1, T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t]
                       for k in range(K) for t in range(1, T + 1))

# Constraints
# Production Capacity Constraints
capacity = [data['capacity']] + [[0] * K for _ in range(T - 1)]
for t in range(2, T + 1):
    for k in range(K):
        capacity[t-1][k] = capacity[t-2][k] + buildcapa[k][t-1]

for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k][t] + buildcapa[k][t] <= capacity[t-1][k]

# Resource Balance Constraints
for t in range(1, T + 1):
    for k in range(K):
        stock_prev = data['stock'][k] if t == 1 else stockhold[k][t-1]
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) +
                     pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K)) +
                     stock_prev >= produce[k][t] + buildcapa[k][t] + stockhold[k][t])

# Demand Satisfaction Constraints
for k in range(K):
    for t in range(2, T + 1):
        problem += produce[k][t] >= data['demand'][k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')