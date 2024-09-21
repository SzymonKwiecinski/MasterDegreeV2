import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Initialize the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total Value"

# Constraint: Total size constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Size Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')