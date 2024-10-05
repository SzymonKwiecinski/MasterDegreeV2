import pulp

# Parse the input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
value = data['value']
size = data['size']
K = len(value)

# Set up the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
isincluded = [pulp.LpVariable(f'isincluded_{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum([value[k] * isincluded[k] for k in range(K)])

# Constraint: Total size does not exceed capacity
problem += (pulp.lpSum([size[k] * isincluded[k] for k in range(K)]) <= C)

# Solve the problem
problem.solve()

# Output the results
output = {
    "isincluded": [int(isincluded[k].varValue) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')