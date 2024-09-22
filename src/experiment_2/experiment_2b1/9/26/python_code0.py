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

# Define problem
K = len(data['manpowerone'])  # number of industries
T = 5  # number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * (produce[k, t] + buildcapa[k, t] for k in range(K) for t in range(1, T + 1)))

# Constraints
# Stock and capacity constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += stockhold[k, t] <= data['stock'][k] + produce[k, t - 1] - data['inputone'][k][k] * produce[k, t] - data['inputtwo'][k][k] * buildcapa[k, t]
        
        if t > 1:
            problem += stockhold[k, t] == stockhold[k, t - 1] + produce[k, t - 1] - data['demand'][k]
        
        problem += produce[k, t] + buildcapa[k, t] <= data['capacity'][k]

# Input constraints
for k in range(K):   
    for j in range(K):
        for t in range(1, T + 1):
            problem += produce[j, t] >= data['inputone'][k][j] * produce[k, t - 1]
            problem += buildcapa[j, t] >= data['inputtwo'][k][j] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
            
# Solve the problem
problem.solve()

# Outputs
produce_output = [[produce[k, t].varValue for t in range(1, T + 1)] for k in range(K)]
buildcapa_output = [[buildcapa[k, t].varValue for t in range(1, T + 1)] for k in range(K)]
stockhold_output = [[stockhold[k, t].varValue for t in range(1, T + 1)] for k in range(K)]

# Print results
results = {
    "produce": produce_output,
    "buildcapa": buildcapa_output,
    "stockhold": stockhold_output
}

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')