import pulp

# Data from JSON input
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Sets and indices
K = range(len(data['benefit']))  # Departments
L = range(len(data['benefit'][0]))  # Locations

# Pulp problem definition
problem = pulp.LpProblem("RelocationOptimization", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in K for l in L), cat='Binary')

# Objective function
total_benefit = pulp.lpSum(data['benefit'][k][l] * islocated[k, l] for k in K for l in L)
communication_cost = pulp.lpSum(
    data['communication'][k][j] * data['cost'][j][m] * islocated[k, l] * islocated[j, m]
    for k in K for j in K for l in L for m in L
)

problem += -total_benefit + communication_cost

# Constraints
# Each department must be located in exactly one city
for k in K:
    problem += pulp.lpSum(islocated[k, l] for l in L) == 1

# No more than three departments can be located in any single city
for l in L:
    problem += pulp.lpSum(islocated[k, l] for k in K) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')