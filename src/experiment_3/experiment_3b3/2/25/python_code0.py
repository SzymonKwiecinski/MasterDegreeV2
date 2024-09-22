import pulp

# Load data
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
T = 5  # Assume 5 years of planning for this example

# Create a problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T-2] for k in range(K))

# Constraints
for t in range(T):
    for k in range(K):
        if t > 0:
            # Production Input Constraints
            problem += produce[k, t] <= data['capacity'][k] + stockhold[k, t-1]
            problem += produce[k, t] <= pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + stockhold[k, t-1]
        # Stock Holding Constraints
        if t > 0:
            problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-1] for j in range(K))
        else:
            problem += stockhold[k, t] == data['stock'][k]
    
    # Manpower Constraints
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']
    
    # Capacity Building Constraints
    if t >= 2:
        for k in range(K):
            problem += data['capacity'][k] <= data['capacity'][k] + buildcapa[k, t-2]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')