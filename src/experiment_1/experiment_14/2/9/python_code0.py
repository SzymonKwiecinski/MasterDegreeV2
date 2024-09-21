import pulp

# Define the data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extracting parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem variable to contain the problem data
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total Value of Items Packed"

# Constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Total Size Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')