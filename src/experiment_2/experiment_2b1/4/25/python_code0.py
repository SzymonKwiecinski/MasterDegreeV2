import json
import pulp

# Load data from JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0,
}

# Constants
K = len(data['stock'])  # Number of industries
T = 3  # Number of time periods (0, 1, 2)

# Create the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(produce[k][T-2] for k in range(K)) + pulp.lpSum(produce[k][T-1] for k in range(K))

# Constraints
for k in range(K):
    for t in range(T):
        # Manpower constraints
        problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) +
                     pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <=
                     data['manpower_limit']), f"Manpower_limit_{t}")

        # Stock balance constraints
        if t > 0:
            problem += (stockhold[k][t-1] + produce[k][t-1] - pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) - buildcapa[k][t-1] >= 0, f"Stock_balance_{k}_{t}")
        
        # Capacity constraints
        problem += (produce[k][t] <= data['capacity'][k] + stockhold[k][t-1], f"Capacity_constraint_{k}_{t}")

# Solve the problem
problem.solve()

# Print the results
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