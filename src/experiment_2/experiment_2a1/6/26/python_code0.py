import pulp
import json

# Input data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Definitions
K = len(data['inputone'])  # Number of industries
T = 5  # Total years for the problem

# Create a problem variable
problem = pulp.LpProblem("Maximize Manpower Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function: Maximize the total manpower requirement over five years
problem += pulp.lpSum(data['manpowerone'][k] * (produce[k][t] + buildcapa[k][t]) for k in range(K) for t in range(T))

# Constraints
for k in range(K):
    for t in range(T):
        # Stock balance constraint
        if t == 0:
            problem += stockhold[k][t] == data['stock'][k] - produce[k][t] + buildcapa[k][t]
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] - produce[k][t] + buildcapa[k][t]

        # Capacity constraint
        problem += produce[k][t] <= data['capacity'][k] + (buildcapa[k][t-2] if t >= 2 else 0)

        # Demand constraints for years 1 to 4
        if t > 0:
            problem += produce[k][t] >= data['demand'][k]

        # Manpower requirements for produce
        problem += produce[k][t] <= data['stock'][k]  # ensure produce does not exceed stock

# Solve the problem
problem.solve()

# Output the results
produce_result = [[produce[k][t].varValue for t in range(T)] for k in range(K)]
buildcapa_result = [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)]
stockhold_result = [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Prepare output in required format
output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

# Output the result
print(json.dumps(output, indent=4))