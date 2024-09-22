import pulp
import json

# Load data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                     [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                     [0.0, 0.0, 2.0, 0.7, 0.0]], 
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(cost)     # Number of cities

# Define the problem
problem = pulp.LpProblem("Department_Relocation_Optimization", pulp.LpMinimize)

# Define decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Define the objective function
problem += pulp.lpSum(
    islocated[k][l] * (
        pulp.lpSum(communication[k][j] * pulp.lpSum(cost[l][m] * islocated[j][m] for m in range(L)) for j in range(K)) - 
        benefit[k][l]
    )
    for k in range(K) 
    for l in range(L)
)

# Department location constraint
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# City capacity constraint
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')