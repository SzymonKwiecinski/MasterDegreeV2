import pulp

# Extracted data from the provided JSON
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Indices
K = range(len(data['benefit']))
L = range(len(data['benefit'][0]))

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in K for l in L), cat='Binary')

# Problem Definition
problem = pulp.LpProblem("Department_Relocation_Minimization", pulp.LpMinimize)

# Objective Function
total_costs = []
for k in K:
    for l in L:
        # Benefit Part
        benefit = data['benefit'][k][l] * islocated[k, l]
        # Communication Cost Part
        comm_cost = sum(data['communication'][k][j] * data['cost'][l][m] * islocated[k, l] for j in K for m in L)
        total_costs.append(comm_cost - benefit)

problem += pulp.lpSum(total_costs)

# Constraints

# Each department is located in exactly one city
for k in K:
    problem += pulp.lpSum(islocated[k, l] for l in L) == 1

# No city can have more than three departments
for l in L:
    problem += pulp.lpSum(islocated[k, l] for k in K) <= 3

# Solve the problem
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')