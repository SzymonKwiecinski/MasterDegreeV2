import pulp
import json

# Given data in JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])  # Number of industries
T = 2  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective Function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T))

# Constraints

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit']

# Capacity constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t]
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t]

        if t < T - 1:
            problem += produce[k][t] + buildcapa[k][t] <= data['capacity'][k]
        else:
            problem += produce[k][t] + buildcapa[k][t] <= data['capacity'][k] + stockhold[k][t-1]

# Input requirements for production
for k in range(K):
    for t in range(T):
        if t > 0:
            for j in range(K):
                problem += produce[k][t] <= data['inputone'][k][j] * stockhold[j][t-1]
                problem += buildcapa[k][t] <= data['inputtwo'][k][j] * stockhold[j][t-1]

# Solve the problem
problem.solve()

# Output the results
results = {
    "produce": [[produce[k][t].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]
}

# Print results
print(json.dumps(results))

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')