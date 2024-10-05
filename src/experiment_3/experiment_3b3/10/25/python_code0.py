import pulp

# Extract data from JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

# Define constants and indices
K = len(data['capacity'])
T = 5  # Assume there are 5 years for this model

# Initialize the problem
problem = pulp.LpProblem("Economy_Production", pulp.LpMaximize)

# Define variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0)

# Objective function: Maximize production in the last two years
problem += pulp.lpSum(produce[k, T] + produce[k, T-1] for k in range(K))

# Constraints
for t in range(1, T+1):
    for k in range(K):
        # Production constraint for each year
        if t == 1:
            problem += produce[k, t] <= data['stock'][k] + data['capacity'][k]
        else:
            problem += produce[k, t] <= stock[k, t-1] + data['capacity'][k]
        
        # Inputs required for production
        if t == 1:
            problem += pulp.lpSum(data['inputone'][k][j] * data['stock'][j] for j in range(K)) >= produce[k, t]
        else:
            problem += pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + stock[k, t-1] >= produce[k, t]
        
        # Manpower limit
        problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + \
                   pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']
        
        # Stock balancing
        if t == 1:
            problem += stock[k, t] == data['stock'][k] + produce[k, t] - \
                       pulp.lpSum(data['inputone'][j][k] * data['stock'][j] for j in range(K))
        else:
            problem += stock[k, t] == stock[k, t-1] + produce[k, t-1] - \
                       pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K))
        
    # Capacity building requirements for years >= 3
    if t >= 3:
        for k in range(K):
            problem += buildcapa[k, t] <= data['capacity'][k] + \
                       pulp.lpSum(data['inputtwo'][k][j] * produce[j, t-2] for j in range(K))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')