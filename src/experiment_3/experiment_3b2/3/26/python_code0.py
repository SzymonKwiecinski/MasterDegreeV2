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

# Constants
K = len(data['manpowerone'])
T = 5  # time periods

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(0, T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * pulp.lpSum(produce[k][t] for t in range(1, T + 1)) +
                      data['manpowertwo'][k] * pulp.lpSum(buildcapa[k][t] for t in range(1, T + 1))
                      for k in range(K)), "Total Manpower Requirement"

# Constraints
# Production and Demand Satisfaction
for t in range(1, T + 1):
    for k in range(K):
        problem += (produce[k][t] + stockhold[k][t-1] >=
                     pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) +
                     data['demand'][k], f"Demand_Satisfaction_{k}_{t}")

# Capacity Constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += (produce[k][t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k][u] for u in range(max(0, t-2))),
                     f"Capacity_Constraint_{k}_{t}")

# Input for Building Capacity
for t in range(1, T + 1):
    for k in range(K):
        problem += (buildcapa[k][t] <= pulp.lpSum(data['inputtwo'][k][j] * produce[j][t] for j in range(K)),
                     f"Building_Capacity_Input_{k}_{t}")

# Stock Flow
for t in range(1, T + 1):
    for k in range(K):
        problem += (stockhold[k][t] == produce[k][t] + stockhold[k][t-1] -
                     pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) - data['demand'][k],
                     f"Stock_Flow_{k}_{t}")

# Initial Stock and Capacity
for k in range(K):
    problem += (stockhold[k][0] == data['stock'][k], f"Initial_Stock_{k}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')