import pulp
import numpy as np

# Data input from the provided JSON
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

# Create a linear programming problem
problem = pulp.LpProblem("Economic_Industries_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                       for k in range(K) for t in range(1, T + 1)), "Total_Manpower_Requirement"

# Constraints
# Production Constraints
for k in range(K):
    for t in range(1, T + 1):
        if t == 1:
            problem += produce[k][t] + stockhold[k][0] - stockhold[k][t] == data['demand'][k], f"Production_Constraint_{k}_{t}"
        else:
            problem += produce[k][t] + stockhold[k][t - 1] - stockhold[k][t] == data['demand'][k], f"Production_Constraint_{k}_{t}"

# Initial Stock
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k], f"Initial_Stock_{k}"

# Capacity Constraints
for k in range(K):
    for t in range(3, T + 1):
        problem += produce[k][t] <= data['capacity'][k] + buildcapa[k][t - 2], f"Capacity_Constraint_{k}_{t}"

# Input Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t - 1] for j in range(K)) + \
                   pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t - 2] for j in range(K)) >= produce[k][t], f"Input_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print decision variables results
for k in range(K):
    for t in range(1, T + 1):
        print(f'produce[{k}][{t}]: {produce[k][t].varValue}, buildcapa[{k}][{t}]: {buildcapa[k][t].varValue}, stockhold[{k}][{t}]: {stockhold[k][t].varValue}')