import pulp

# Data input
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])
T = 3  # Considering a planning horizon of 3 years

# Initialize the problem
problem = pulp.LpProblem("Production_Capacity_Planning", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T-2, T))

# Constraints
for t in range(T):
    for k in range(K):
        # Stock balance constraints
        if t == 0:
            problem += (stockhold[k, t] == data['stock'][k] + produce[k, t] 
                        - pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K))
                        - pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)))
        else:
            problem += (stockhold[k, t] == stockhold[k, t-1] + produce[k, t] 
                        - pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K))
                        - pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)))

        # Capacity constraints
        if t == 0:
            problem += produce[k, t] <= data['capacity'][k]
        else:
            problem += produce[k, t] <= (data['capacity'][k] + pulp.lpSum(buildcapa[k, t-2] for s in range(t-1)))

    # Manpower constraint
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K))
                <= data['manpower_limit'])

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')