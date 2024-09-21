import pulp

# Data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the Linear Programming problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize sum of values * binary variables
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "MaximizeValue"

# Constraint: Sum of sizes * binary variables should not exceed the capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "TotalSizeConstraint"

# Solve the problem
problem.solve()

# Output the value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')