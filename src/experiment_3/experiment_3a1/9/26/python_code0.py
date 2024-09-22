import pulp
import json

# Data in JSON format
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
T = 5  # Time horizon

# Create the problem
problem = pulp.LpProblem("Industry_Production_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(1, T + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K) for t in range(1, T + 1)) + \
           pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K) for t in range(1, T + 1))

# Constraints
# Production Constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) + 
            (stockhold[k][t-1] if t > 1 else data['stock'][k]) >= data['demand'][k], 
            f"ProductionConstraint_{k}_{t}"
        )
        
        problem += (
            produce[k][t] <= data['capacity'][k] + (stockhold[k][t-1] if t > 1 else data['stock'][k]),
            f"CapacityConstraint_{k}_{t}"
        )

# Capacity Building Constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += (
            buildcapa[k][t] * pulp.lpSum(data['inputtwo'][k][j] for j in range(K)) + 
            (stockhold[k][t-1] if t > 1 else data['stock'][k]) >= data['capacity'][k], 
            f"CapacityBuildingConstraint_{k}_{t}"
        )

# Stock Constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += (
            stockhold[k][t] == (data['stock'][k] if t == 1 else stockhold[k][t-1]) - produce[k][t],
            f"StockConstraint_{k}_{t}"
        )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')