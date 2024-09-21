import pulp

# Data from the provided JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Number of items
K = len(values)

# Create a linear programming problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("item", range(K), 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "Total Value"

# Constraints
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "Total Size Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')