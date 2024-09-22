import pulp

# Parse the problem data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extract data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem instance
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Create decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize value
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

# Capacity constraint: Do not exceed max size
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

# Solve the problem
problem.solve()

# Extract and print the results
isincluded = [pulp.value(x[k]) for k in range(K)]
print(f'isincluded = {isincluded}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')