import pulp

# Define data from JSON
data = {
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Define constants
K = len(data["benefit"])  # Number of departments
L = len(data["benefit"][0])  # Number of cities

# Initialize variables
benefit = data["benefit"]
communication = data["communication"]
cost = data["cost"]

# Initialize problem
problem = pulp.LpProblem("DepartmentRelocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function
problem += pulp.lpSum([
    islocated[k, l] * (benefit[k][l] - pulp.lpSum([communication[k][j] * cost[l][m] * islocated[j, m] for j in range(K) for m in range(L)]))
    for k in range(K) for l in range(L)
])

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# Each city cannot have more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve problem
problem.solve()

# Collect results
solution = {
    "islocated": [
        [pulp.value(islocated[k, l]) for l in range(L)] for k in range(K)
    ]
}

# Print solution
print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')