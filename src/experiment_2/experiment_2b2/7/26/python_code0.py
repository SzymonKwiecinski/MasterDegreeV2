import pulp

# Data Input
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

K = len(data["capacity"])  # Number of industries
T = 5  # Number of years

# Initialize LP Problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    data["manpowerone"][k] * produce[(k, t)] + data["manpowertwo"][k] * buildcapa[(k, t)] for k in range(K) for t in range(T)
)

# Constraints per year and industry
for t in range(T):
    for k in range(K):
        # Production and capacity constraints
        if t == 0:  # Initial constraints using stock and initial capacity
            problem += produce[(k, t)] + buildcapa[(k, t)] <= data["capacity"][k] + data["stock"][k]
        else:
            problem += produce[(k, t)] + buildcapa[(k, t)] <= stockhold[(k, t-1)] + data["capacity"][k]

        # Stock balance constraints
        if t > 0:  # No stockholding constraints at t=0
            problem += stockhold[(k, t)] == (
                stockhold[(k, t-1)] +
                produce[(k, t-1)] -
                sum(data["inputone"][i][k] * produce[(i, t-1)] for i in range(K)) -
                data["demand"][k]
            )

# Solve the problem
problem.solve()

# Results
produce_out = [[pulp.value(produce[(k, t)]) for t in range(T)] for k in range(K)]
buildcapa_out = [[pulp.value(buildcapa[(k, t)]) for t in range(T)] for k in range(K)]
stockhold_out = [[pulp.value(stockhold[(k, t)]) for t in range(T)] for k in range(K)]

output_format = {
    "produce": produce_out,
    "buildcapa": buildcapa_out,
    "stockhold": stockhold_out
}

print(output_format)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')