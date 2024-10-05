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

K = len(data['inputone'])  # Number of industries
T = 5  # Planning horizon (years)

# Problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("Produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
stock = pulp.LpVariable.dicts("Stock", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K) for t in range(1, T+1)) + \
           pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(1, T+1))

# Constraints
for k in range(K):
    for t in range(1, T+1):
        # Production Balance
        problem += produce[k, t] + stock[k, t-1] == \
                   pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + stock[k, t]
        
        # Capacity Build
        problem += (buildcapa[k, t] * pulp.lpSum(data['inputtwo'][k][j] for j in range(K))) + stock[k, t-1] >= \
                    data['demand'][k]

        # Stock Evolution
        problem += stock[k, t] == stock[k, t-1] + produce[k, t] - data['demand'][k] + buildcapa[k, t]

    # Initial stock constraint
    problem += stock[k, 0] == data['stock'][k]

    # Capacity Constraints
    problem += data['capacity'][k] >= pulp.lpSum(buildcapa[k, t] for t in range(1, T+1))

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')