import pulp

# Given data
data = {
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    "communication": [
        [0.0, 0.0, 1.0, 1.5, 0.0],
        [0.0, 0.0, 1.4, 1.2, 0.0],
        [1.0, 1.4, 0.0, 0.0, 2.0],
        [1.5, 1.2, 0.0, 2.0, 0.7],
        [0.0, 0.0, 2.0, 0.7, 0.0]
    ],
    "cost": [
        [5, 14, 13],
        [15, 5, 9],
        [13, 9, 10]
    ]
}

benefit = data["benefit"]
communication = data["communication"]
cost = data["cost"]

num_departments = len(communication)  # K
num_cities = len(cost)  # L

# Initialize the problem
problem = pulp.LpProblem("Relocation_Problem", pulp.LpMinimize)

# Decision variables
islocated = [[pulp.LpVariable(f"islocated_{k}_{l}", cat="Binary") for l in range(num_cities)] for k in range(num_departments)]

# Objective function
total_benefit = pulp.lpSum(benefit[k][l] * islocated[k][l] for k in range(num_departments) for l in range(len(benefit[0])))
total_communication_cost = pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[k][l] * islocated[j][m]
    for k in range(num_departments)
    for j in range(num_departments)
    for l in range(num_cities)
    for m in range(num_cities)
)
problem += total_communication_cost - total_benefit

# Constraints
# Each department must be located in exactly one city
for k in range(num_departments):
    problem += pulp.lpSum(islocated[k][l] for l in range(num_cities)) == 1

# No city can have more than three departments
for l in range(num_cities):
    problem += pulp.lpSum(islocated[k][l] for k in range(num_departments)) <= 3

# Solve the problem
problem.solve()

# Prepare the solution
solution = {"islocated": [[int(islocated[k][l].varValue) for l in range(num_cities)] for k in range(num_departments)]}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')