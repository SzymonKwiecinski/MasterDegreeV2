import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
value = data['value']
size = data['size']

# Number of items
K = range(len(value))

# Create the linear programming problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
isincluded = pulp.LpVariable.dicts("isincluded", K, 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum([value[k] * isincluded[k] for k in K]), "TotalValue"

# Constraints
problem += pulp.lpSum([size[k] * isincluded[k] for k in K]) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')