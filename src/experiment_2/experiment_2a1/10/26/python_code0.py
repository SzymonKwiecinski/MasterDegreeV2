import pulp
import json

# Input data
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['inputone'])  # Number of industries
T = 5  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("Produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("BuildCapacity", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("StockHold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * (produce[k, t] + buildcapa[k, t]) for k in range(K) for t in range(T))

# Constraints
# Manpower & Demand Constraints
for t in range(T):
    for k in range(K):
        if t == 0:
            problem += produce[k, t] + stockhold[k, t] == data['stock'][k] + data['capacity'][k]
        else:
            problem += produce[k, t] + stockhold[k, t] == data['demand'][k] + (stockhold[k, t-1] if t > 0 else 0) + data['capacity'][k]

        if t < T - 2:
            problem += buildcapa[k, t] <= data['inputtwo'][k][k] * (stockhold[k, t-2] if t - 2 >= 0 else 0)

# Add input requirements
for t in range(1, T):
    for k in range(K):
        for j in range(K):
            if j != k:
                problem += (produce[k, t] >= data['inputone'][k][j] * produce[j, t-1])

# Stock hold constraints
for t in range(1, T):
    for k in range(K):
        problem += stockhold[k, t] >= stockhold[k, t-1] + produce[k, t-1] - data['demand'][k]

# Solve the problem
problem.solve()

# Extract results
produce_result = [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

output