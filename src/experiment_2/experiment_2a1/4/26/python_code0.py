import pulp
import numpy as np
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
K = len(data['demand'])  # Number of industries
T = 5  # Number of years

# Create a LP problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("Produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("BuildCapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("StockHold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective function: Maximize total manpower requirement over five years
total_manpower = pulp.lpSum(data['manpowerone'][k] * (produce[k][t] + buildcapa[k][t]) for k in range(K) for t in range(T))
problem += total_manpower

# Constraints
for k in range(K):
    for t in range(T):
        # Satisfy demand
        problem += produce[k][t] + stockhold[k][t] >= data['demand'][k] if t > 0 else produce[k][t] + stockhold[k][t] >= 0
        
        # Stocks from previous year
        if t > 0:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t-1] - data['demand'][k] if t < T - 1 else stockhold[k][t] == stockhold[k][t-1] + produce[k][t-1] - data['demand'][k]
        
        # Capacity constraints
        problem += produce[k][t] <= data['capacity'][k] + stockhold[k][t]

        # Building capacity constraints
        if t < T - 1:
            problem += buildcapa[k][t] * data['manpowertwo'][k] <= produce[k][t]

# Solve the problem
problem.solve()

# Prepare results
result = {
    "produce": [[produce[k][t].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]
}

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the results
print(json.dumps(result))