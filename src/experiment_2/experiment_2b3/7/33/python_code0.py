import pulp

# Parse input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Initialize the problem
problem = pulp.LpProblem('Knapsack', pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize total value
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

# Constraint: Total size should not exceed capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

# Solve the problem
problem.solve()

# Prepare the output
isincluded = [int(x[k].varValue) for k in range(K)]
output = {
    "isincluded": isincluded
}

# Output result
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')