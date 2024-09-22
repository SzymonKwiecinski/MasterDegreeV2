import pulp

# Data from JSON
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

K = len(data["inputone"])
T = 5

# Initialize the problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function: Maximize manpower over five years
problem += pulp.lpSum(data["manpowerone"][k] * produce[(k, t)] + data["manpowertwo"][k] * buildcapa[(k, t)]
                      for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    for k in range(K):
        # Flow constraints - conservation of units
        rhs_flow = (produce[(k, t)] + (stockhold[(k, t - 1)] if t > 0 else data["stock"][k]))
        lhs_flow = (data["demand"][k] + stockhold[(k, t)] + pulp.lpSum(data["inputone"][k][j] * produce[(j, t)] for j in range(K)))
        problem += (rhs_flow == lhs_flow)
        
        # Capacity constraints
        rhs_capacity = produce[(k, t)] + pulp.lpSum(data["inputtwo"][k][j] * buildcapa[(j, t - 2)] for j in range(K)) if t >= 2 else 0
        lhs_capacity = (data["capacity"][k] if t == 0 else pulp.lpSum(produce[(k, t_prime)] for t_prime in range(t)))
        problem += (rhs_capacity <= lhs_capacity)

# Solve the problem
problem.solve()

# Prepare the output format
output = {
    "produce": [[produce[(k, t)].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[(k, t)].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[(k, t)].varValue for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')