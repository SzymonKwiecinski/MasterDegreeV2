import pulp

# Parsing data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables: x_k is 1 if item k is included, otherwise 0
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize the sum of values of included items
problem += pulp.lpSum([values[k] * x[k] for k in range(K)])

# Constraint: Total size of included items must not exceed capacity C
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C

# Solve the problem
problem.solve()

# Output the results
isincluded = [int(x[k].varValue) for k in range(K)]
output = {"isincluded": isincluded}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')