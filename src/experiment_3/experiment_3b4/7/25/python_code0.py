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

K = 3  # Number of industries
T = 3  # Number of years

# Initialize the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Objective
problem += pulp.lpSum(produce[k, T-2] + produce[k, T-1] for k in range(K))

# Constraints

# Capacity Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] + buildcapa[k, t] <= data['capacity'][k]

# Stock Balance Constraints
for k in range(K):
    for t in range(T):
        problem += (stockhold[k, t+1] == stockhold[k, t] + produce[k, t] 
                    - pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K))
                    - pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)))

# Production and Building Requirements
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] 
                           for k in range(K)) <= data['manpower_limit'])

# Initial Conditions
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')