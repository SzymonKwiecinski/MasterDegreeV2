import pulp

# Data initialization based on provided JSON format
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(communication)  # Number of entities
L = len(benefit[0])     # Number of locations

# Problem initialization
problem = pulp.LpProblem("Location_Assignment", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat=pulp.LpBinary)

# Objective Function
objective = pulp.lpSum(
    -benefit[k][l] * islocated[k, l] for k in range(K) for l in range(L)
) + pulp.lpSum(
    communication[k][j] * cost[m][l] * islocated[k, l] * islocated[j, m]
    for k in range(K)
    for j in range(K)
    for l in range(L)
    for m in range(L)
)

problem += objective

# Constraints
# Each entity must be located in exactly one location
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# Each location can have at most 3 entities
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')