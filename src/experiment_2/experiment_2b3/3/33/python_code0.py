import pulp

# Problem data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Define the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Number of items
K = len(data['value'])

# Decision variables
x = [pulp.LpVariable(f'x{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize total value
problem += pulp.lpSum(data['value'][k] * x[k] for k in range(K))

# Constraint: Total size must not exceed capacity C
problem += pulp.lpSum(data['size'][k] * x[k] for k in range(K)) <= data['C']

# Solve the problem
problem.solve()

# Output results
isincluded = [int(x[k].varValue) for k in range(K)]
output_format = {
    "isincluded": isincluded
}

print(output_format)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')