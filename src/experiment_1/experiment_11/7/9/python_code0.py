import pulp

# Data from JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the model
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

# Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "TotalSizeConstraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')