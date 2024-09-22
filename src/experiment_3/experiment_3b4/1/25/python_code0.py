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
K = len(data['capacity']) # Number of types
T = 3  # Total number of years

# Create the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T-2, T)), "Maximize Production"

# Constraints

# Input requirements for production
for k in range(K):
    for t in range(T-1):
        problem += produce[k, t+1] <= pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)), f"InputReq_{k}_{t}"

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_{t}"

# Capacity constraints
for k in range(K):
    problem += produce[k, 0] + buildcapa[k, 0] <= data['capacity'][k], f"InitialCapacity_{k}"
    for t in range(1, T):
        problem += produce[k, t] + buildcapa[k, t] <= data['capacity'][k] + pulp.lpSum(data['inputtwo'][j][k] * buildcapa[j, t-1] for j in range(K)), f"Capacity_{k}_{t}"

# Stock dynamics
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += stockhold[k, t] == data['stock'][k] + produce[k, t] - pulp.lpSum(data['inputone'][j][k] * produce[j, t+1] for j in range(K)) - buildcapa[k, t], f"Stock_{k}_{t}"
        else:
            problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - pulp.lpSum(data['inputone'][j][k] * produce[j, t+1] for j in range(K)) - buildcapa[k, t], f"Stock_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')