import pulp

# Data from the JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem instance
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Create binary decision variables
x = pulp.LpVariable.dicts("x", range(K), 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

# Constraint for maximum capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')