import pulp

# Define the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Extract data from JSON
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "manpower_limit": 470000000.0
}

# Unpacking data
inputone = data["inputone"]
manpowerone = data["manpowerone"]
inputtwo = data["inputtwo"]
manpowertwo = data["manpowertwo"]
stock = data["stock"]
initial_capacity = data["capacity"]
manpower_limit = data["manpower_limit"]
K = len(inputone)  # Number of industries
T = 5  # Number of years in planning horizon

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Objective: Maximize total production in the last two years
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in [T-2, T-1])

# Constraints
# Initial stocks
for k in range(K):
    problem += stockhold[k, 0] == stock[k]

# Capacity and production constraints
for k in range(K):
    for t in range(T):
        if t < 2:
            problem += produce[k, t] <= initial_capacity[k]
        else:
            problem += produce[k, t] <= initial_capacity[k] + pulp.lpSum(buildcapa[k, t_prime] for t_prime in range(t-2+1))
        
        # Balance equation for stocks
        problem += stockhold[k, t+1] == stockhold[k, t] + produce[k, t] - buildcapa[k, t] - pulp.lpSum(produce[m, t] * inputone[k][m] for m in range(K))

# Manpower constraint
for t in range(T):
    problem += pulp.lpSum(produce[k, t] * manpowerone[k] + buildcapa[k, t] * manpowertwo[k] for k in range(K)) <= manpower_limit

# Solve the problem
problem.solve()

# Construct the output format
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T+1)] for k in range(K)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')