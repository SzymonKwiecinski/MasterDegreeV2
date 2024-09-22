import pulp

# Load data
data = {
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data["benefit"]
communication = data["communication"]
cost = data["cost"]

K = len(communication)
L = len(cost)

# Create a problem instance
problem = pulp.LpProblem("DepartmentRelocation", pulp.LpMinimize)

# Decision variables
islocated = [[pulp.LpVariable(f'islocated_{k}_{l}', cat='Binary') for l in range(L)] for k in range(K)]

# Objective function
total_benefit = pulp.lpSum(islocated[k][l] * benefit[k][l] for k in range(K) for l in range(L))
total_communication_cost = pulp.lpSum(
    islocated[k][l] * islocated[j][m] * communication[k][j] * cost[l][m]
    for k in range(K) for l in range(L) for j in range(K) for m in range(L)
)
problem += -total_benefit + total_communication_cost  # Minimize total cost (negative benefit plus communication cost)

# Contraints
# Each department is located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# No city has more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Prepare the output
islocated_solution = [[pulp.value(islocated[k][l]) for l in range(L)] for k in range(K)]

output = {
    "islocated": islocated_solution,
}

# Display the results
print(output)

# Display the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')