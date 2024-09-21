import pulp

# Data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Parameters
C = data['C']
value = data['value']
size = data['size']
K = len(value)

# Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum([value[k] * x[k] for k in range(K)])

# Constraints
problem += pulp.lpSum([size[k] * x[k] for k in range(K)]) <= C

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')