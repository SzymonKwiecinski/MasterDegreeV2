import pulp
import json

# Data input
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Parameters
K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Define the problem
problem = pulp.LpProblem("Economy_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective function: Maximize total manpower requirement over five years
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    for k in range(K):
        # Demand constraint
        if t > 0:
            problem += pulp.lpSum(produce[k][t] + stockhold[k][t-1] - stockhold[k][t] - data['demand'][k]) >= 0
        
        # Capacity constraints
        if t < T - 1:
            problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) + stockhold[k][t] <= data['capacity'][k] + buildcapa[k][t]

        # Stock balance
        if t > 0:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t-1] - data['demand'][k] - buildcapa[k][t-1]
        else:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t] - data['demand'][k] - buildcapa[k][t]

# Solve the problem
problem.solve()

# Print the output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')