import pulp

# Read input data from JSON, assumed to be provided as a json string
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

K = len(capacity)  # Number of industries
T = 5  # Planning period

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("Produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("StockHold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function: Maximize total manpower requirement over the planning period
problem += pulp.lpSum((produce[k, t] * manpowerone[k] + buildcapa[k, t] * manpowertwo[k])
                      for k in range(K) for t in range(T))

# Constraints

# Initial stock and capacity constraints for year 0
for k in range(K):
    problem += pulp.lpSum(produce[k, 0]) <= capacity[k]
    problem += stockhold[k, 0] == stock[k] + produce[k, 0] - buildcapa[k, 0]

# Stock constraints for subsequent years
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - demand[k] - buildcapa[k, t]

# Production and capacity constraints for all years
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += produce[k, t] <= capacity[k]
        else:
            problem += produce[k, t] <= (capacity[k] + pulp.lpSum(buildcapa[k, t - 2] if t - 2 >= 0 else 0))

# Input constraints
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(inputone[j][k] * produce[j, t] for j in range(K)) + \
                   pulp.lpSum(inputtwo[j][k] * buildcapa[j, t] for j in range(K)) <= produce[k, t]

# Solve the problem
problem.solve()

# Extract and format the solution
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')