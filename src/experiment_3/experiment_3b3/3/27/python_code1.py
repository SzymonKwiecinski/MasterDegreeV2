import pulp

# Data from the JSON format
benefit = [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]]
communication = [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]]
cost = [[5, 14, 13], [15, 5, 9], [13, 9, 10]]

# Indices for departments and cities
K = len(benefit)  # Departments
L = len(benefit[0])  # Cities

# Initialize the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective Function
objective_terms = []

for k in range(K):
    for l in range(L):
        internal_sum = pulp.lpSum(
            communication[k][j] * pulp.lpSum(cost[l][m] * islocated[j, m] for m in range(L))
            for j in range(K)
        )
        term = islocated[k, l] * (internal_sum - benefit[k][l])
        objective_terms.append(term)

problem += pulp.lpSum(objective_terms)

# Constraints
# Each department can be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No city can accommodate more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the solution
islocated_result = [[pulp.value(islocated[k, l]) for l in range(L)] for k in range(K)]

print(f'islocated = {islocated_result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')