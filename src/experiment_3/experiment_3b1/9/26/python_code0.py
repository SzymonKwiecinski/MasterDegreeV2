import pulp
import numpy as np
import json

data = json.loads("{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'demand': [60000000.0, 60000000.0, 30000000.0]}")

# Unpack data
inputone = np.array(data['inputone'])
manpowerone = np.array(data['manpowerone'])
inputtwo = np.array(data['inputtwo'])
manpowertwo = np.array(data['manpowertwo'])
initial_stock = np.array(data['stock'])
initial_capacity = np.array(data['capacity'])
demand = np.array(data['demand'])

K = len(manpowerone)
T = 5

# Create the LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K) for t in range(T))

# Production Constraints
for k in range(K):
    for t in range(1, T):
        problem += produce[k][t] <= initial_capacity[k] + stockhold[k][t-1], f"Prod_Capacity_Constraint_k{K}_t{t}"
        problem += produce[k][t] == pulp.lpSum(inputone[k][j] * produce[j][t-1] for j in range(K)) + stockhold[k][t-1], f"Prod_Input_Constraint_k{K}_t{t}"

# Capacity Building Constraints
for k in range(K):
    for t in range(T):
        problem += buildcapa[k][t] <= initial_capacity[k] + pulp.lpSum(inputtwo[k][j] * buildcapa[j][t-1] for j in range(K)), f"Cap_Build_Capacity_Constraint_k{K}_t{t}"
        problem += buildcapa[k][t] <= manpowertwo[k], f"Cap_Build_Manpower_Constraint_k{K}_t{t}"

# Stock Constraints
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - demand[k] + buildcapa[k][t-1], f"Stock_Constraint_k{K}_t{t}"

# Initial Conditions
for k in range(K):
    problem += stockhold[k][0] == initial_stock[k], f"Initial_Stock_k{k}"
    problem += stockhold[k][0] >= initial_capacity[k], f"Initial_Capacity_k{k}"

# Solve the problem
problem.solve()

# Print the Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')