import pulp

# Problem data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # number of departments
L = len(cost)     # number of cities

# Problem definition
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function
benefits_term = pulp.lpSum(islocated[k, l] * benefit[k][l] for k in range(K) for l in range(L) if l < len(benefit[k]))

communication_costs_term = pulp.lpSum(
    islocated[k, l] * islocated[j, m] * communication[k][j] * cost[l][m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
)

problem += -benefits_term + communication_costs_term

# Constraints
# Each department must be allocated to exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No more than three departments in any city
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve problem
problem.solve()

# Solution
islocated_solution = [[pulp.value(islocated[k, l]) for l in range(L)] for k in range(K)]

output = {
    "islocated": islocated_solution
}

# Print solution
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')