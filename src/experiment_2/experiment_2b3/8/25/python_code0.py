import pulp

# Data from JSON
data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'manpower_limit': 470000000.0}

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
manpower_limit = data['manpower_limit']

K = len(stock)  # number of industries
T = 4  # years to consider (0, 1, 2, 3 to plan for 4 periods)

# Define LP problem
problem = pulp.LpProblem("Maximize Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T-1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(2, T))

# Constraints

# Initial stock and capacity constraints for year 0
for k in range(K):
    problem += stockhold[k, 0] == stock[k]
    problem += produce[k, 0] <= capacity[k]


# Capacity constraints
for k in range(K):
    for t in range(1, T):
        if t > 1:
            problem += produce[k, t] <= capacity[k] + pulp.lpSum(buildcapa[k, t - d] for d in [2] if t - d >= 0)
        else:
            problem += produce[k, t] <= capacity[k]

# Stock constraints
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k, t] == stockhold[k, t-1] - pulp.lpSum(inputone[i][k] * produce[i, t] for i in range(K)) + produce[k, t]

# Manpower constraints
for t in range(T):
    problem += (
        pulp.lpSum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K) if (t < T - 1)) <= manpower_limit
    )

# Solve the problem
problem.solve()

# Process Output
produce_result = [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k, t]) if t < T - 1 else 0 for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]

output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')