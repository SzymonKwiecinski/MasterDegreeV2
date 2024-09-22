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

# Problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Variables
K = 3
T = 5
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(1, T+1))

# Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += (produce[k, t] + stockhold[k, t-1] - stockhold[k, t]
                    == pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K))
                    + data['stock'][k]
                    + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-2] if t-2 >= 0 else 0 for j in range(K)))

    problem += (data['capacity'][k] + pulp.lpSum(buildcapa[k, t] for t in range(1, T+1))
                >= data['demand'][k])

# Initial Stock Constraint
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')