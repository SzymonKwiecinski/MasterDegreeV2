import pulp

# Data input
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

K = len(demand)  # Number of industries
T = 5  # Planning horizon (5 years)

# LP Problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K) for t in range(T))

# Constraints
for k in range(K):
    for t in range(T):
        # Capacity constraints
        if t == 0:
            problem += produce[k, t] <= capacity[k]
        else:
            problem += produce[k, t] <= (capacity[k] + pulp.lpSum(buildcapa[k, i] for i in range(max(0, t-2))))

        # Stock constraints
        if t == 0:
            problem += stockhold[k, t] == stock[k] + produce[k, t] - buildcapa[k, t] - (0 if t == 0 else demand[k])
        else:
            problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - buildcapa[k, t] - (demand[k] if t > 0 else 0)

        # Input constraints
        for j in range(K):
            if t > 0:
                problem += inputone[k][j] * produce[k, t] + inputtwo[k][j] * buildcapa[k, t] <= produce[j, t-1]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[produce[k, t].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[k, t].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[k, t].varValue for t in range(T)] for k in range(K)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')