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

# Constants
K = len(data['inputone'])  # Number of industries
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective function: Maximize total manpower requirement
total_manpower = pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K) for t in range(T)) + \
                 pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K) for t in range(T))
problem += total_manpower

# Constraints
# Year 0 constraints (initial stock and capacity)
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k]
    problem += produce[k][0] + stockhold[k][0] <= data['capacity'][k]

# Year t constraints for t > 0
for t in range(1, T):
    for k in range(K):
        # Production and build capacity must meet demand
        problem += (produce[k][t] + stockhold[k][t-1] - stockhold[k][t] >= data['demand'][k])
        # Inputs required from previous year
        for j in range(K):
            problem += (produce[k][t] >= pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)))
        
        # Building capacity
        problem += (buildcapa[k][t] >= pulp.lpSum(data['inputtwo'][k][j] * produce[j][t-1] for j in range(K)))

# Capacity constraints for future years
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k][t] <= data['capacity'][k] + buildcapa[k][t-1] - produce[k][t]
        
# Solve the problem
problem.solve()

# Output results
produce_result = [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]

output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')