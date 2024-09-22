import pulp

# Input data
data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'demand': [60000000.0, 60000000.0, 30000000.0]}

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

K = len(inputone)  # Number of industries
T = 5  # Number of years

# Define the LP problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective: maximize total manpower requirement over 5 years
problem += pulp.lpSum((produce[k, t] * manpowerone[k] + buildcapa[k, t] * manpowertwo[k]) for k in range(K) for t in range(T))

# Constraints

# Initial stock
for k in range(K):
    problem += stockhold[k, 0] == stock[k]

# Capacity constraints
for k in range(K):
    for t in range(T):
        previous_capacity = capacity[k] if t == 0 else produce[k, t-1] + buildcapa[k, t-1] + stockhold[k, t-1]
        problem += produce[k, t] <= previous_capacity

# Demand and stock constraints
for k in range(K):
    for t in range(1, T):
        problem += produce[k, t] + stockhold[k, t-1] >= demand[k]

# Input constraints for production and capacity
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(inputone[k][j] * produce[j, t] for j in range(K)) + pulp.lpSum(inputtwo[k][j] * buildcapa[j, t] for j in range(K)) <= produce[k, t] + buildcapa[k, t]

# Solve the problem
problem.solve()

# Extract the results
produce_result = [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]

output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')