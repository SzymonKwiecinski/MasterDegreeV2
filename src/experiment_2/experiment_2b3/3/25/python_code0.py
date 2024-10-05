import pulp

# Data from JSON
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "manpower_limit": 470000000.0,
}

K = len(data["inputone"])
T = 5  # Assuming we plan for 5 years

# Decision variables for production, building capacity, and stockholding
produce = pulp.LpVariable.dicts("Produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("StockHold", (range(K), range(T+1)), lowBound=0)

# LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Objective function: Maximize production in the last two years (years 4 and 5)
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T-2, T))

# Constraints
for k in range(K):
    for t in range(T):
        # Capacity constraints
        if t == 0:
            problem += (produce[k][t] <= data["capacity"][k] + stockhold[k][t])
        else:
            additional_capacity = pulp.lpSum(buildcapa[k][t-2]) if t >= 2 else 0
            problem += (produce[k][t] <= stockhold[k][t] + additional_capacity)
        
        # Stock update constraint
        if t == 0:
            problem += (stockhold[k][t+1] == data["stock"][k] - produce[k][t])
        else:
            problem += (stockhold[k][t+1] == stockhold[k][t] - produce[k][t])

        # Input requirements for production and building capacity
        problem += (pulp.lpSum(data["inputone"][k][j] * produce[j][t] for j in range(K)) +
                    pulp.lpSum(data["inputtwo"][k][j] * buildcapa[j][t] for j in range(K)) <= stockhold[k][t])

    # Manpower constraints
    for t in range(T):
        problem += (pulp.lpSum(data["manpowerone"][k] * produce[k][t] for k in range(K)) +
                    pulp.lpSum(data["manpowertwo"][k] * buildcapa[k][t] for k in range(K)) <= data["manpower_limit"])

# Solve the problem
problem.solve()

# Extract results
results = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T+1)] for k in range(K)],
}

import json
print(json.dumps(results, indent=4))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')