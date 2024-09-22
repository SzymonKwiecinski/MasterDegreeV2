import pulp
import json

# Data provided in JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['manpowerone'])  # Number of industries
T = 3  # Number of years (this can vary based on problem specifics)

# Create pulp problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("Produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("StockHold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k, T] for k in range(K)) + pulp.lpSum(produce[k, T - 1] for k in range(K))

# Constraints for production and capacity building
for k in range(K):
    for t in range(1, T + 1):
        # Stock balance constraint
        if t == 1:
            problem += stockhold[k, t] == data['stock'][k] + produce[k, t] - pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K))
        else:
            problem += stockhold[k, t] == stockhold[k, t - 1] + produce[k, t] - pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K))

        # Capacity constraints
        problem += produce[k, t] + stockhold[k, t] <= data['capacity'][k]

# Manpower constraints for production
for t in range(1, T + 1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) <= data['manpower_limit']

# Manpower constraints for capacity building
for k in range(K):
    for t in range(1, T + 1):
        problem += buildcapa[k, t] <= data['capacity'][k]  # Fixed reference to data['capacity']

# Solve the problem
problem.solve()

# Prepare the result
result = {
    "produce": [[pulp.value(produce[k, t]) for t in range(1, T + 1)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(1, T + 1)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(1, T + 1)] for k in range(K)]
}

# Print the results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')