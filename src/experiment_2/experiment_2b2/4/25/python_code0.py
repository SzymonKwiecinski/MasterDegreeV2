import pulp

# Data
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "manpower_limit": 470000000.0
}

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
manpower_limit = data['manpower_limit']

K = len(capacity)  # Number of industries
T = 3  # Number of years to consider

# Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Initial stock
for k in range(K):
    problem += stockhold[(k, 0)] == stock[k]

# Capacity constraints
for k in range(K):
    for t in range(T):
        problem += produce[(k, t)] + buildcapa[(k, t)] <= capacity[k]
        capacity[k] += pulp.lpSum(buildcapa[(k_prime, t-2)] * inputtwo[k_prime][k] for k_prime in range(K)) if t >= 2 else 0

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(produce[(k, t)] * manpowerone[k] + buildcapa[(k, t)] * manpowertwo[k] for k in range(K)) <= manpower_limit

# Stock constraints
for k in range(K):
    for t in range(T):
        problem += stockhold[(k, t+1)] == stockhold[(k, t)] + produce[(k, t)] - pulp.lpSum(produce[(k_prime, t)] * inputone[k_prime][k] for k_prime in range(K))

# Objective: Maximize production in last two years
objective_expr = pulp.lpSum(produce[(k, t)] for k in range(K) for t in range(T-2, T))
problem += objective_expr

# Solve
problem.solve()

# Output
output = {
    "produce": [[pulp.value(produce[(k, t)]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[(k, t)]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[(k, t)]) for t in range(T+1)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')