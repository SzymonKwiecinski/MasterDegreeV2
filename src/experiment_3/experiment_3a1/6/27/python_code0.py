import pulp
import json

# Data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0],
                     [0.0, 0.0, 1.4, 1.2, 0.0],
                     [1.0, 1.4, 0.0, 0.0, 2.0],
                     [1.5, 1.2, 0.0, 2.0, 0.7],
                     [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13],
             [15, 5, 9],
             [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(benefit[0])  # Number of cities
M = len(cost[0])  # Number of cost cities (assuming cost is given for the same cities as benefit)

# Problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[k][l]
    for k in range(K) for j in range(K) for l in range(L) for m in range(M)
) - pulp.lpSum(
    benefit[k][l] * islocated[k][l]
    for k in range(K) for l in range(L)
)

# Constraints
# Each department must be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# No city can house more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Each department can be either relocated or remain in London (city index 0)
for k in range(K):
    problem += islocated[k][0] == 1  # Assuming the first city (index 0) is London

# Solve the problem
problem.solve()

# Output
islocated_matrix = [[pulp.value(islocated[k][l]) for l in range(L)] for k in range(K)]
print("islocated = ", islocated_matrix)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')