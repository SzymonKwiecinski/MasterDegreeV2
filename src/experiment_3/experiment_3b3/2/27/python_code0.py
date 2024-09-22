import pulp

# Data
benefit = [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]]
communication = [
    [0.0, 0.0, 1.0, 1.5, 0.0],
    [0.0, 0.0, 1.4, 1.2, 0.0],
    [1.0, 1.4, 0.0, 0.0, 2.0],
    [1.5, 1.2, 0.0, 2.0, 0.7],
    [0.0, 0.0, 2.0, 0.7, 0.0],
]
cost = [[5, 14, 13], [15, 5, 9], [13, 9, 10]]

# Sets
K = range(len(benefit))  # departments
L = range(len(benefit[0]))  # cities

# Problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in K for l in L), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    benefit[k][l] * islocated[k, l] -
    pulp.lpSum(
        communication[k][j] *
        pulp.lpSum(cost[l][m] * islocated[j, m] for m in L)
        for j in K
    )
    for k in K for l in L
)

# Constraints
# Each department must be located in exactly one city
for k in K:
    problem += pulp.lpSum(islocated[k, l] for l in L) == 1

# No city can have more than three departments
for l in L:
    problem += pulp.lpSum(islocated[k, l] for k in K) <= 3

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')