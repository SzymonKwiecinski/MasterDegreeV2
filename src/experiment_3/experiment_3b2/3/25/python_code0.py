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
    'manpower_limit': 470000000.0
}

K = len(data['stock'])
T = 2  # Assume T is 2 for the time periods

# Create the problem
problem = pulp.LpProblem('Maximize_Production', pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (k for k in range(K)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[(k, T-1)] + produce[(k, T)] for k in range(K))

# Constraints
# Capacity constraint
for k in range(K):
    for t in range(T):
        problem += produce[(k, t)] + buildcapa[(k, t)] <= data['capacity'][k], f'Capacity_Constraint_{k}_{t}'

# Manpower constraint
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)] for k in range(K)) <= data['manpower_limit'], f'Manpower_Constraint_{t}'

# Stock constraints
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[(j, t)] + data['inputtwo'][k][j] * buildcapa[(j, t)] for j in range(K)) <= stockhold[k] + produce[(k, t)], f'Stock_Constraint_{k}_{t}'

# Stock initialization and transition
for k in range(K):
    problem += stockhold[k] == data['stock'][k], f'Initial_Stock_{k}'
    for t in range(T-1):
        problem += stockhold[k] == stockhold[k] - pulp.lpSum(data['inputone'][j][k] * produce[(k, t)] for j in range(K)) - pulp.lpSum(data['inputtwo'][j][k] * buildcapa[(k, t)] for j in range(K)), f'Stock_Transition_{k}_{t}'

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')