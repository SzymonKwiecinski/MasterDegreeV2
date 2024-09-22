import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Define the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Number of items
K = len(data['value'])

# Decision variables
x = [pulp.LpVariable(f"x{k}", cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['value'][k] * x[k] for k in range(K))

# Constraints
problem += pulp.lpSum(data['size'][k] * x[k] for k in range(K)) <= data['C']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')