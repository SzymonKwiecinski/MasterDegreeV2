import pulp
import json

# Load the data from JSON format
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                      [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                      [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Parameters
K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of cities

# Create the LP problem
problem = pulp.LpProblem("Relocation_Problem", pulp.LpMinimize)

# Decision variable islocated[k][l]
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

# Calculate the objective
objective = pulp.lpSum([islocated[k][l] * benefit[k][l] for k in range(K) for l in range(L)]) \
            - pulp.lpSum([islocated[k][l] * islocated[j][m] * communication[k][j] * cost[l][m] 
                           for k in range(K) for j in range(K) 
                           for l in range(L) for m in range(L) if k != j])  # Fixing the multiplication issue

problem += objective

# Constraints
# Each department is located in exactly one city
for k in range(K):
    problem += pulp.lpSum([islocated[k][l] for l in range(L)]) == 1

# No city can have more than three departments
for l in range(L):
    problem += pulp.lpSum([islocated[k][l] for k in range(K)]) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')