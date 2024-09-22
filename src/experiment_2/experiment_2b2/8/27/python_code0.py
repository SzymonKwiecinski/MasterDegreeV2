import pulp

# Data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

# Problem definition
problem = pulp.LpProblem("DepartmentRelocation", pulp.LpMinimize)

# Dimensions
K = len(benefit)  # Number of departments
L = len(benefit[0])  # Number of possible cities

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective Function
total_benefit = pulp.lpSum(islocated[k, l] * benefit[k][l] for k in range(K) for l in range(L))
total_communication_cost = pulp.lpSum(
    islocated[k, l] * islocated[j, m] * communication[k][j] * cost[l][m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
)

problem += total_communication_cost - total_benefit, "Total Cost"

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1, f"Department_{k}_Location"

# No city can host more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3, f"City_{l}_Capacity"

# Solve
problem.solve()

# Extracting the solution
solution = {
    "islocated": [[pulp.value(islocated[k, l]) for l in range(L)] for k in range(K)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')