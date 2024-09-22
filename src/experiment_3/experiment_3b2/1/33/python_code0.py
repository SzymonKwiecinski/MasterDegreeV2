import pulp

# Given data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
value = data['value']
size = data['size']

# Create the linear programming problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
K = len(value)
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(value[k] * isincluded[k] for k in range(K)), "TotalValue"

# Constraint
problem += pulp.lpSum(size[k] * isincluded[k] for k in range(K)) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')