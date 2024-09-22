import pulp

# Input data
data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'manpower_limit': 470000000.0}

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
manpower_limit = data['manpower_limit']

K = len(inputone)  # Number of industries
T = 3  # We'll consider years 0, 1, 2

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Objective Function: Maximize production in year 2
problem += pulp.lpSum(produce[k, 2] for k in range(K))

# Constraints

# Initial stock
for k in range(K):
    problem += stockhold[k, 0] == stock[k]

# Production and capacity constraints
for t in range(T):
    for k in range(K):
        # Total output constraints
        problem += pulp.lpSum(inputone[k][j] * produce[j, t] for j in range(K)) + \
                   pulp.lpSum(inputtwo[k][j] * buildcapa[j, max(0, t-2)] for j in range(K)) + stockhold[k, t] == \
                   produce[k, t] + buildcapa[k, t] + stockhold[k, t+1]

        # Capacity constraints
        if t == 0:
            problem += produce[k, t] <= capacity[k]
        else:
            problem += produce[k, t] <= capacity[k] + pulp.lpSum(buildcapa[k, tt] for tt in range(t-2+1))

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K)) <= manpower_limit

# Solve the problem
problem.solve()

# Collect results
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T + 1)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')