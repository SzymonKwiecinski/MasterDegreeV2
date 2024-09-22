import pulp
import json

# Data from the provided JSON format
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0],
                     [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(cost)     # Number of cities

# Create a linear programming problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function
objective = pulp.lpSum([
    pulp.lpSum([
        communication[k][j] * cost[j][l] * islocated[k][l] 
        for j in range(K) for l in range(L) if l != j
    ]) - pulp.lpSum(benefit[k][l] * islocated[k][l] for l in range(L))
    for k in range(K)
])

problem += objective

# Constraints
# Each department must be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# No city can host more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')