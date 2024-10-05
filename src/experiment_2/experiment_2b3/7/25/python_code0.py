import pulp

# Defining the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Extract data from INPUT
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

K = len(inputone)
T = 5

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective Function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T-2, T)), "Total_Production_Last_Two_Years"

# Constraints
for t in range(T):
    for k in range(K):
        if t == 0:
            stockhold[k][t] == stock[k] + produce[k][t] - pulp.lpSum(inputone[k][j] * produce[j][t] for j in range(K)) - pulp.lpSum(inputtwo[k][j] * buildcapa[j][t] for j in range(K))
        else:
            stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - pulp.lpSum(inputone[k][j] * produce[j][t] for j in range(K)) - pulp.lpSum(inputtwo[k][j] * buildcapa[j][t] for j in range(K))

for t in range(T):
    for k in range(K):
        if t < 2:
            produce[k][t] <= capacity[k]
        else:
            produce[k][t] <= capacity[k] + buildcapa[k][t-2]

    problem += pulp.lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K)) <= manpower_limit

# Solve the problem
problem.solve()

# Prepare OUTPUT
output = {
    "produce": [[produce[k][t].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[k][t].varValue for t in range(T)] for k in range(K)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')