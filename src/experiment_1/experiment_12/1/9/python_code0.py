import pulp

# Data from the JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Number of items
K = len(data['value'])

# Create the LP problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables: x_k = 1 if item k is included in the knapsack, 0 otherwise
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize the total value
problem += pulp.lpSum(data['value'][k] * x[k] for k in range(K)), "Total Value"

# Constraint: The total size must not exceed the capacity
problem += pulp.lpSum(data['size'][k] * x[k] for k in range(K)) <= data['C'], "Total Size Constraint"

# Solve the problem
problem.solve()

# Print the optimal objective value
print(f'Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>')