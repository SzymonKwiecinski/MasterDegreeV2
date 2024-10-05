import pulp
import json

# Data from the provided JSON
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Sets and parameters
K = len(data['stock'])  # Number of industries
T = 3  # Assuming 3 years for the model according to the provided data

# Creating the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')
capacity = pulp.LpVariable.dicts("capacity", (range(K), range(T)), lowBound=0, cat='Continuous')

# Initial Conditions
for k in range(K):
    stockhold[k][0] = data['stock'][k]
    capacity[k][0] = data['capacity'][k]

# Objective Function
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T - 2, T))

# Production Constraints
for t in range(1, T):
    for k in range(K):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j][t - 1] for j in range(K)) +
                     stockhold[k][t - 1] >= produce[k][t] + buildcapa[k][t] + stockhold[k][t])

# Capacity Constraints
for t in range(T):
    for k in range(K):
        problem += (produce[k][t] + buildcapa[k][t] <= capacity[k][t])

# Manpower Constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] + 
                            data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= 
                 data['manpower_limit'])

# Capacity Dynamics
for t in range(2, T):
    for k in range(K):
        problem += (capacity[k][t] == capacity[k][t - 1] + buildcapa[k][t - 2])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')