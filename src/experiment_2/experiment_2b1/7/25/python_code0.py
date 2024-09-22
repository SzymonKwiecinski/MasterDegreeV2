import json
import pulp

# Input data from the provided JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])  # The number of industries
T = 2  # The number of years we consider for production

# Define the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective function: maximize production in the last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T))

# Constraints
# 1. Capacity constraints
for k in range(K):
    for t in range(T):
        problem += (stockhold[k][t-1] + data['capacity'][k] + 
                    pulp.lpSum(produce[j][t-1] * data['inputone'][j][k] for j in range(K)) -
                    produce[k][t] - buildcapa[k][t] == stockhold[k][t], f"Stock_Constraint_{k}_{t}")

# 2. Stock constraints
for k in range(K):
    stockhold[k][0] = data['stock'][k]  # Initial stock at year 0

# 3. Manpower constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) +
                pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= 
                data['manpower_limit'], f"Manpower_Limit_{t}")

# Solve the problem
problem.solve()

# Collecting the output
produce_output = [[produce[k][t].varValue for t in range(T)] for k in range(K)]
buildcapa_output = [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)]
stockhold_output = [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]

# Prepare the output in the required format
output = {
    "produce": produce_output,
    "buildcapa": buildcapa_output,
    "stockhold": stockhold_output
}

# Print the result
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')