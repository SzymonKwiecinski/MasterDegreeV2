import pulp
import numpy as np
import json

data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])
T = 2  # Considering the time horizon to be 2 years

# Create the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T)), "Total_Production"

# Constraints
# Capacity constraints for production
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += produce[k, t] <= data['capacity'][k] + data['stock'][k], f"Capacity_Production_Year_{t}_Industry_{k}"
        else:
            problem += produce[k, t] <= data['capacity'][k] + stockhold[k, t-1], f"Capacity_Production_Year_{t}_Industry_{k}"

# Manpower constraints for production
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(manpowerone[k] * produce[k, t] for k in range(K)) <= data['manpower_limit'], "Manpower_Production"

# Inputs for production
for k in range(K):
    for t in range(T):
        if t > 0:
            problem += pulp.lpSum(inputone[k][j] * produce[j, t-1] for j in range(K)) >= produce[k, t], f"Input_Production_Year_{t}_Industry_{k}"

# Capacity building constraints
for k in range(K):
    for t in range(T):
        if t < T - 1:
            problem += pulp.lpSum(inputtwo[k][j] * buildcapa[j, t] for j in range(K)) >= buildcapa[k, t], f"Input_Building_Capa_Year_{t}_Industry_{k}"
            problem += pulp.lpSum(manpowertwo[k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], "Manpower_Building_Capa_Production"
        
# Stock constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            stockhold[k, t] = data['stock'][k] + produce[k, t]
        else:
            stockhold[k, t] = stockhold[k, t-1] + produce[k, t-1] - pulp.lpSum(inputone[k][j] * produce[j, t-1] for j in range(K))

# Solve the problem
problem.solve()

# Output results
output_produce = [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)]
output_buildcapa = [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)]
output_stockhold = [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]

output = {
    "produce": output_produce,
    "buildcapa": output_buildcapa,
    "stockhold": output_stockhold
}

# Print results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')