import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Problem
problem = pulp.LpProblem("Maximize_Total_Manpower_Requirement", pulp.LpMaximize)

# Sets
K = 3  # Number of industries
T = 5  # Number of years

# Decision variables
produce = pulp.LpVariable.dicts("produce", [(k, t) for k in range(K) for t in range(T)], lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", [(k, t) for k in range(K) for t in range(T)], lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", [(k, t) for k in range(K) for t in range(T)], lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(T))

# Initial Stock Condition
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]

# Initial Capacity Condition
for k in range(K):
    capacity_k = data['capacity'][k]

# Production and Stock Balance Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += stockhold[k, 0] + produce[k, 0] == (pulp.lpSum(data['inputone'][k][j] * produce[j, 0] for j in range(K)) +
                                                            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, 0] for j in range(K)) +
                                                            data['demand'][k] + stockhold[k, 0])
        else:
            problem += stockhold[k, t-1] + produce[k, t] == (pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) +
                                                             pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) +
                                                             data['demand'][k] + stockhold[k, t])

# Capacity Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k, i] for i in range(t))

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')