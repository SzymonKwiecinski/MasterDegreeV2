import pulp

# Data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

# Capacity constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')