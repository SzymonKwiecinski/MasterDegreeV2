import pulp

# Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
manpower_limit = data['manpower_limit']

K = len(capacity)  # Number of industries
T = 4  # Planning for 4 years

# Linear Programming Problem
problem = pulp.LpProblem("Economy_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective: Maximize total production in the last two years (year 3 and 4)
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(2, T))

# Constraints

# Initial stock and capacity constraints for year 0
for k in range(K):
    problem += (stockhold[k][0] == stock[k] - pulp.lpSum(inputone[k][j] * produce[j][0] for j in range(K))
                - pulp.lpSum(inputtwo[k][j] * buildcapa[j][0] for j in range(K)))
    problem += produce[k][0] + buildcapa[k][0] <= capacity[k]

# Capacity and stock constraints for subsequent years
for t in range(1, T):
    for k in range(K):
        problem += (stockhold[k][t] == stockhold[k][t - 1] + produce[k][t - 1]
                    - pulp.lpSum(inputone[k][j] * produce[j][t] for j in range(K))
                    - pulp.lpSum(inputtwo[k][j] * buildcapa[j][t] for j in range(K)))
        
        new_capacity = capacity[k] + (buildcapa[k][t - 2] if t >= 2 else 0)
        problem += produce[k][t] + buildcapa[k][t] <= new_capacity

# Manpower constraints
for t in range(T):
    problem += (pulp.lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K))
                <= manpower_limit)

# Solve the problem
problem.solve()

# Results
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')