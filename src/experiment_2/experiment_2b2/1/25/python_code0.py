import pulp

# Data from <DATA>
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])  # Number of industries
T = 4  # Considering years 0, 1, 2, 3

# Define LP Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective: Maximize production in the last two years (year 2 and 3)
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(2, T))

# Constraints
for t in range(T):
    if t > 0:
        # Stock balance equation
        for k in range(K):
            problem += (stockhold[k][t] == stockhold[k][t-1] + produce[k][t-1] - 
                        pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K))
                        - buildcapa[k][t])
    else:
        # Initial stock condition
        for k in range(K):
            problem += (stockhold[k][t] == data['stock'][k])
    
    # Production capacity constraint
    for k in range(K):
        if t == 0:
            problem += produce[k][t] <= data['capacity'][k]
        else:
            problem += produce[k][t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k][t-t_2] for t_2 in range(2) if t-t_2 >= 0)
    
    # Total Manpower Constraint
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                           for k in range(K)) <= data['manpower_limit'])

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')