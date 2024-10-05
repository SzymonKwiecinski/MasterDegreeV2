import pulp

# Data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0],
                      [0.0, 0.0, 1.4, 1.2, 0.0],
                      [1.0, 1.4, 0.0, 0.0, 2.0],
                      [1.5, 1.2, 0.0, 2.0, 0.7],
                      [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13],
             [15, 5, 9],
             [13, 9, 10]]
}

# Sets
K = list(range(len(data['benefit'])))  # Set of departments
L = list(range(len(data['benefit'][0])))  # Set of cities

# Parameters
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

# Problem
problem = pulp.LpProblem("DepartmentRelocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (K, L), 0, 1, pulp.LpBinary)

# Objective Function
objective = pulp.lpSum(
    pulp.lpSum(
        communication[k][j] * cost[l][m] * islocated[j][m]
        for j in K for m in L
    ) - benefit[k][l] * islocated[k][l]
    for k in K for l in L
)

problem += objective

# Constraints
# Each department must be located in exactly one city
for k in K:
    problem += pulp.lpSum(islocated[k][l] for l in L) == 1

# A city can accommodate at most three departments
for l in L:
    problem += pulp.lpSum(islocated[k][l] for k in K) <= 3

# Solve the problem
problem.solve()

# Output the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the Solution
solution = [[int(islocated[k][l].varValue) for l in L] for k in K]
print("islocated =", solution)