import pulp

# Provided JSON data
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

# Constants
K = len(data["capacity"])
T = 5

# Initialize the LP problem
problem = pulp.LpProblem("Economy_Optimization", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function: Maximize total manpower requirement over five years
problem += pulp.lpSum(
    [data["manpowerone"][k] * produce[(k, t)] + data["manpowertwo"][k] * buildcapa[(k, t)] for k in range(K) for t in range(T)]
)

# Stock Balance and Demand constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += produce[(k, t)] + stockhold[(k, t)] == data["stock"][k] + data["capacity"][k]
        else:
            problem += produce[(k, t)] + stockhold[(k, t)] == produce[(k, t - 1)] + stockhold[(k, t - 1)] + buildcapa[(k, t - 2)] if t >= 2 else produce[(k, t - 1)] + stockhold[(k, t - 1)]
            problem += produce[(k, t)] >= data["demand"][k]

# Capacity constraints
for k in range(K):
    for t in range(T):
        problem += produce[(k, t)] <= data["capacity"][k] + pulp.lpSum(
            [buildcapa[(k, past_t)] for past_t in range(max(0, t-1))])

# Solve the problem
problem.solve()

# Extract solution
output = {
    "produce": [[pulp.value(produce[(k, t)]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[(k, t)]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[(k, t)]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')