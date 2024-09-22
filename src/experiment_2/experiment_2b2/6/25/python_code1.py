import pulp

# Extract data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

K = len(data['capacity'])
T = 4

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Objective function: Maximize total production in the last two years (T-2, T-1)
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T-2, T)), "TotalProduction"

# Initial stock constraint for year 0
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k], f"Initial_Stock_{k}"

# Capacity constraint for production
for k in range(K):
    for t in range(T):
        build_capacity = pulp.lpSum(buildcapa[k, t_prime] for t_prime in range(max(0, t-2), t))
        problem += produce[k, t] <= data['capacity'][k] + build_capacity, f"Capacity_{k}_{t}"

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"ManpowerLimit_{t}"

# Stock balance constraints
for k in range(K):
    for t in range(T):
        inputs_used = pulp.lpSum(data['inputone'][k][j] * produce[j, t] + data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K))
        problem += stockhold[k, t+1] == stockhold[k, t] + produce[k, t] - inputs_used, f"StockBalance_{k}_{t}"

# Solve the LP problem
problem.solve()

# Output results
result = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T+1)] for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')