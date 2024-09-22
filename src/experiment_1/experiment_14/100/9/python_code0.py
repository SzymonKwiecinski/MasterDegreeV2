import pulp

# Load data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Define the decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Define the objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

# Define the constraints
problem += (pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C), "TotalSizeConstraint"

# Solve the problem
problem.solve()

# Output the results
print(f'Optimal Solution Status: {pulp.LpStatus[problem.status]}')
for k in range(K):
    print(f'x_{k}: {pulp.value(x[k])}')

print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')