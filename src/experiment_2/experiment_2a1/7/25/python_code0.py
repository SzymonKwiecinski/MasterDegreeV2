import pulp
import numpy as np
import json

data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'manpower_limit': 470000000.0}

K = len(data['stock'])
T = 3  # Assume we are modeling for 3 years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Define decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(1, T)) 

# Constraints for production and manpower
for k in range(K):
    for t in range(T):
        # Stock carried forward
        if t == 0:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t] - pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K))
            problem += stockhold[k][t] >= 0
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K))
            problem += stockhold[k][t] >= 0

        # Manpower constraints
        manpower_used = pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K))
        problem += manpower_used <= data['manpower_limit']

# Build capacity constraints
for k in range(K):
    for t in range(T-1):  # We can't build capacity in the last year for the next year
        problem += buildcapa[k][t] <= data['capacity'][k] - (pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K)) if t < T-1 else 0)

# Solve the problem
problem.solve()

# Collect results
produce_result = np.zeros((K, T))
buildcapa_result = np.zeros((K, T))
stockhold_result = np.zeros((K, T))

for k in range(K):
    for t in range(T):
        produce_result[k][t] = pulp.value(produce[k][t])
        buildcapa_result[k][t] = pulp.value(buildcapa[k][t])
        stockhold_result[k][t] = pulp.value(stockhold[k][t])

# Output results
output = {
    "produce": produce_result.tolist(),
    "buildcapa": buildcapa_result.tolist(),
    "stockhold": stockhold_result.tolist()
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')