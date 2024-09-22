import pulp

# Load data
data = {
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(cost)     # Number of possible locations

# Initialize the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function: Total cost = -Benefit + Communication cost
total_cost = pulp.lpSum(
    -benefit[k][l] * islocated[k, l]
    for k in range(K) for l in range(L)
) + pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[k, l] * islocated[j, m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
)

problem += total_cost

# Constraints
# Each department is located exactly in one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No more than 3 departments in any one city
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Extract results
result = {
    "islocated": [[pulp.value(islocated[k, l]) for l in range(L)] for k in range(K)],
}

# Print results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')