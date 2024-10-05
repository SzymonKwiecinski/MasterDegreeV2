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

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

# Constants
K = len(capacity)  # Number of industries
T = 5  # Number of years

# Problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective: Maximize total manpower over the five years
problem += pulp.lpSum((manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t]) for k in range(K) for t in range(T))

# Capacity constraints
for t in range(T):
    for k in range(K):
        if t == 0:
            problem += produce[k, t] + buildcapa[k, t] <= capacity[k]
        else:
            problem += produce[k, t] + buildcapa[k, t] <= capacity[k] + pulp.lpSum(buildcapa[k, t - 2] for k in range(K) if t - 2 >= 0)

# Stock constraints
for t in range(T):
    for k in range(K):
        if t == 0:
            problem += produce[k, t] + stock[k] == demand[k] + pulp.lpSum(inputone[j][k] * produce[j, t] for j in range(K)) + stockhold[k, t]
        else:
            problem += produce[k, t] + stockhold[k, t - 1] == demand[k] + pulp.lpSum(inputone[j][k] * produce[j, t] for j in range(K)) + stockhold[k, t]

# Solve the problem
problem.solve()

# Output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")