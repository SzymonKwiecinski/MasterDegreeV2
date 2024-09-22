import pulp
import json

# Input data
data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'manpower_limit': 470000000.0}

# Parameters
K = len(data['inputone'])  # number of industries
T = 2  # number of years

# Create problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(produce[k, T] for k in range(K)) + pulp.lpSum(produce[k, T - 1] for k in range(K))

# Constraints
# 1. Production constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += stockhold[k, t - 1] + produce[k, t] - pulp.lpSum(data['inputone'][k][j] * produce[j, t - 1] for j in range(K)) - stockhold[k, t] == data['stock'][k] if t == 1 else 0
        problem += stockhold[k, t - 1] + produce[k, t] - pulp.lpSum(data['inputone'][k][j] * produce[j, t - 1] for j in range(K)) - stockhold[k, t] >= 0 if t > 1 else 0

# 2. Manpower constraints for production
for t in range(1, T + 1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) <= data['manpower_limit']

# 3. Capacity expansion constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += capacity[k] + pulp.lpSum(buildcapa[k, t_prime] for t_prime in range(1, T + 1)) - pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) >= 0

# Solve the problem
problem.solve()

# Extract the results
produce_res = [[produce[k, t].varValue for t in range(1, T + 1)] for k in range(K)]
buildcapa_res = [[buildcapa[k, t].varValue for t in range(1, T + 1)] for k in range(K)]
stockhold_res = [[stockhold[k, t].varValue for t in range(1, T + 1)] for k in range(K)]

# Output results
output = {
    "produce": produce_res,
    "buildcapa": buildcapa_res,
    "stockhold": stockhold_res
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')