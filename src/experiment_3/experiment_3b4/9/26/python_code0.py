import pulp

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

K = 3  # Industries
T = 5  # Years

# Problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
capacity = {k: [data['capacity'][k] for _ in range(T+2)] for k in range(K)}

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] 
                      for k in range(K) for t in range(T))

# Constraints

# Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= capacity[k][t]

# Capacity Building Constraints
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) <= produce[k, t]

# Stock Balance Constraints
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]  # Initial stock
    for t in range(1, T):
        problem += stockhold[k, t] == (stockhold[k, t-1] + produce[k, t] 
                                       - pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) 
                                       - data['demand'][k])

# Capacity Update Constraints
for k in range(K):
    for t in range(4):  # till T-2 considering t+2 condition
        capacity[k][t+2] = capacity[k][t+1] + buildcapa[k, t]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')