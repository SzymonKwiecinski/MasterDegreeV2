import pulp
import json

# Input Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Constants
K = len(data['inputone'])
T = 3  # Assume we are looking at 3 years for simplicity

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T))  # Total production across all industries and years

# Constraints
# Manpower constraint
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit'], f'Manpower_Constraint_Yr_{t}'

# Input and Stock constraints for production
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += produce[k][t] <= data['stock'][k], f'Production_Stock_Constraint_{k}_Yr_{t}'
        else:
            problem += produce[k][t] <= data['capacity'][k] + stockhold[k][t-1], f'Production_Capacity_Constraint_{k}_Yr_{t}'
    
        # Update stocks
        stockhold[k][t] = pulp.lpSum(stockhold[k][t-1] + produce[k][t-1] - produce[k][t] for t in range(T))
        
# Inputs required for production from previous year
for k in range(K):
    for t in range(1, T):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) >= produce[k][t], f'Input_Constraint_{k}_Yr_{t}'

# Inputs required for building capacity from previous year
for k in range(K):
    for t in range(1, T):
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K)) >= buildcapa[k][t], f'Build_Capacity_Constraint_{k}_Yr_{t}'

# Solve the problem
problem.solve()

# Output the results
produce_result = [[produce[k][t].varValue for t in range(T)] for k in range(K)]
buildcapa_result = [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)]
stockhold_result = [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]

output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')