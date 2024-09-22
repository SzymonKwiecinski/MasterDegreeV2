import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)  # Changed the name to remove space

# Number of items
K = len(data['value'])

# Decision variables
x = [pulp.LpVariable(f"x_{k}", cat='Binary') for k in range(K)]  # Changed variable names to remove space

# Objective function
problem += pulp.lpSum(data['value'][k] * x[k] for k in range(K))

# Constraints
problem += pulp.lpSum(data['size'][k] * x[k] for k in range(K)) <= data['C']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')