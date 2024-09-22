import json
import pulp

# Input Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['capacity'])  # Number of industries
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("Produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("StockHold", (range(K), range(T)), lowBound=0)

# Objective function: maximize total manpower requirement
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    for k in range(K):
        if t == 0:
            problem += produce[k][t] + stockhold[k][t] == data['stock'][k] + data['capacity'][k]
        else:
            problem += produce[k][t] + stockhold[k][t] == stockhold[k][t-1] + data['capacity'][k] + (produce[k][t-1] if t > 0 else 0)
        
        # Demand satisfaction for years 1 to 5
        if t > 0:
            problem += produce[k][t] >= data['demand'][k]

        # Manpower constraints
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K)) <= data['stock'][k] + data['capacity'][k]
        
        # Stock balance
        if t > 0:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t-1] - data['demand'][k]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

# Output results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')