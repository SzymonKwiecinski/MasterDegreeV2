import pulp
import json

# Load data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Define parameters
K = len(data['manpowerone'])
T = 5

# Create the problem
problem = pulp.LpProblem("Economic_Planning", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("Produce", (range(K), range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", (range(K), range(1, T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("StockHold", (range(K), range(1, T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K) for t in range(1, T+1))

# Constraints
# Production and Capacity Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k][t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k][tau] for tau in range(1, t-1))

# Input Constraints for Production
for k in range(K):
    for t in range(1, T+1):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) <= pulp.lpSum(stockhold[j][tau] for tau in range(t))

# Input Constraints for Capacity Building
for k in range(K):
    for t in range(1, T+1):
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K)) <= pulp.lpSum(stockhold[j][tau] for tau in range(t))

# Stock Flow Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += stockhold[k][t] == data['stock'][k] + pulp.lpSum(produce[k][tau] - buildcapa[k][tau] - data['demand'][k] for tau in range(1, t+1))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')