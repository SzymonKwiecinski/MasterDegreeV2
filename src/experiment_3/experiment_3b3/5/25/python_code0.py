import pulp

# Data from the JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Constants
K = len(data['stock'])
T = 5

# Problem
problem = pulp.LpProblem("EconomicProduction", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("Produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
stock = pulp.LpVariable.dicts("Stock", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T] for k in range(K))

# Constraints

# Initial conditions for stock
for k in range(K):
    problem += stock[k, 0] == data['stock'][k]

# Production Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k, t] <= data['capacity'][k] + (stock[k, t-1] if t > 1 else data['stock'][k])

# Input Constraints
for k in range(K):
    for t in range(2, T+1):
        problem += produce[k, t] <= pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + \
                   pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-2] for j in range(K))

# Manpower Constraints
for t in range(1, T+1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']

# Stock Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += stock[k, t] == (stock[k, t-1] if t > 1 else data['stock'][k]) + produce[k, t-1] - \
                   pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K)) - (buildcapa[k, t-1] if t > 1 else 0)

# Capacity Building Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += buildcapa[k, t] <= pulp.lpSum(data['inputtwo'][k][j] * produce[j, t-1] for j in range(K)) + \
                   (stock[k, t-1] if t > 1 else data['stock'][k])

# Solve the problem
problem.solve()

# Print objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')