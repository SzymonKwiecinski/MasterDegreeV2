import pulp

# Parse the input data
data = {
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data["benefit"]
communication = data["communication"]
cost = data["cost"]

num_departments = len(benefit)
num_cities = len(benefit[0])

# Create a Linear Programming problem
problem = pulp.LpProblem("DepartmentRelocation", pulp.LpMinimize)

# Decision Variables
islocated = [[pulp.LpVariable(f'islocated_{k}_{l}', cat='Binary') for l in range(num_cities)] for k in range(num_departments)]

# Objective Function
objective = pulp.lpSum([
    -benefit[k][l] * islocated[k][l]
    + pulp.lpSum([
        communication[k][j] * cost[l][m] * islocated[j][m]
        for j in range(num_departments) for m in range(num_cities)
    ])
    for k in range(num_departments) for l in range(num_cities)
])

problem += objective

# Constraints
# Each department must be in exactly one city
for k in range(num_departments):
    problem += (pulp.lpSum([islocated[k][l] for l in range(num_cities)]) == 1)

# No more than 3 departments in any city
for l in range(num_cities):
    problem += (pulp.lpSum([islocated[k][l] for k in range(num_departments)]) <= 3)

# Solve the problem
problem.solve()

# Output the result
solution = {
    "islocated": [[int(pulp.value(islocated[k][l])) for l in range(num_cities)] for k in range(num_departments)],
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')