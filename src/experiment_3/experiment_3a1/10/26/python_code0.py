import pulp
import json

# Input data from the given JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])  # Number of industries (k)
T = 5  # Time period (years)

# Define the problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Define variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (k for k in range(K)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K) for t in range(1, T + 1)) + \
           pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(1, T + 1))

# Initial stock conditions
for k in range(K):
    stockhold[k] = data['stock'][k]

# Constraints
for t in range(1, T + 1):
    for k in range(K):
        # Production Capacity Constraint
        problem += produce[k, t] + stockhold[k] >= data['demand'][k] + stockhold[k]

        # Stock Holding Constraint
        problem += stockhold[k] == stockhold[k] + produce[k, t] - data['demand'][k]

        # Input Constraint for Production
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + stockhold[k] >= produce[k, t]

        # Input Constraint for Building Capacity
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-1] for j in range(K)) + stockhold[k] >= buildcapa[k, t]

        # Capacity Constraint
        problem += produce[k, t] + buildcapa[k, t] <= data['capacity'][k] + stockhold[k]

# Solve the problem
problem.solve()

# Output results
produce_results = [[pulp.value(produce[k, t]) for t in range(1, T + 1)] for k in range(K)]
buildcapa_results = [[pulp.value(buildcapa[k, t]) for t in range(1, T + 1)] for k in range(K)]
stockhold_results = [pulp.value(stockhold[k]) for k in range(K)]

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')