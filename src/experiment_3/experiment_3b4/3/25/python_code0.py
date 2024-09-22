import pulp

# Data
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
T = 5  # Assuming 5 years as the time horizon

# Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Objective function
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T-1, T+1))

# Constraints
initial_stock = data['stock']
initial_capacity = data['capacity']
inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
manpower_limit = data['manpower_limit']

# Initial conditions
for k in range(K):
    problem += stockhold[k, 0] == initial_stock[k]
    for t in range(1, 3):
        problem += pulp.lpSum(produce[j, t-1] * inputtwo[k][j] for j in range(K)) == 0  # Capacity doesn't change for t < 3

for t in range(1, T + 1):
    # Capacity Constraint
    for k in range(K):
        problem += produce[k, t] + buildcapa[k, t] <= initial_capacity[k]

    # Stock Constraint
    for k in range(K):
        problem += stockhold[k, t - 1] + pulp.lpSum(produce[j, t - 1] * inputone[k][j] for j in range(K)) >= produce[k, t] + buildcapa[k, t]

    # Manpower Constraint
    problem += pulp.lpSum(produce[k, t] * manpowerone[k] + buildcapa[k, t] * manpowertwo[k] for k in range(K)) <= manpower_limit

# Capacity Update for t >= 3
for t in range(3, T + 1):
    for k in range(K):
        problem += initial_capacity[k] + pulp.lpSum(buildcapa[j, t - 2] * inputtwo[k][j] for j in range(K)) == initial_capacity[k]

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')