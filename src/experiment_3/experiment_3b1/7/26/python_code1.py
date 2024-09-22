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

# Model parameters
K = len(data['manpowerone'])
T = 5

# Create the problem
problem = pulp.LpProblem("Maximize_Production_and_Capacity_Building", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T + 1)), lowBound=0)

# Objective function
problem += (pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K) for t in range(1, T + 1)) +
             pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(1, T + 1))), "Total_Profit"

# Capacity constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (produce[k, t] <= stock[k, t - 1] + data['capacity'][k] +
                     pulp.lpSum(data['inputone'][k][j] * produce[j, t - 1] for j in range(K)) +
                     pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t - 2] for j in range(K) if t > 2), f"ProductionConstraint_{k}_{t}")
        
        problem += (buildcapa[k, t] <= stock[k, t - 1] + data['capacity'][k] +
                     pulp.lpSum(data['inputtwo'][k][j] * produce[j, t - 1] for j in range(K)), f"BuildCapacityConstraint_{k}_{t}")

# Stock update constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (stock[k, t] == stock[k, t - 1] + produce[k, t] - data['demand'][k] + buildcapa[k, t], f"StockUpdate_{k}_{t}")

# Set initial stock
for k in range(K):
    problem += (stock[k, 0] == data['stock'][k], f"InitialStock_{k}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')