import pulp

# Provided data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

# Dimensions
K = len(benefit)     # Number of departments
L = len(benefit[0])  # Number of locations

# Initialize the Linear Program
problem = pulp.LpProblem("Department Relocation Problem", pulp.LpMaximize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function
benefit_expression = pulp.lpSum(benefit[k][l] * islocated[k, l] for k in range(K) for l in range(L))
comm_costs_expression = pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[k, l] * islocated[j, m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
)
problem += benefit_expression - comm_costs_expression

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No city can host more than 3 departments
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Extracting the solution
solution = {
    "islocated": [[int(islocated[k, l].varValue) for l in range(L)] for k in range(K)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')