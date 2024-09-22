import pulp
import numpy as np

# Data from the provided JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                       for k in range(K) for t in range(1, T + 1)), "Total Manpower Requirement"

# Constraints
# Production Constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + stockhold[k][t-1] >= 
                     data['demand'][k] + stockhold[k][t]), f"Production_Constraint_k{K}_t{t}"

# Capacity Building Constraints
for t in range(1, T + 1):
    for k in range(K):
        problem += (pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K)) + stockhold[k][t] >= 
                     produce[k][t+1] if t < T else 0), f"Capacity_Building_Constraint_k{K}_t{t}"

# Initial Conditions
for k in range(K):
    problem += (stockhold[k][0] == data['stock'][k]), f"Initial_Stock_k{k}"

# Capacity Update Condition
for k in range(K):
    problem += (data['capacity'][k] == data['capacity'][k] + pulp.lpSum(buildcapa[k][t] for t in range(1, T + 1))), f"Capacity_Update_k{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')