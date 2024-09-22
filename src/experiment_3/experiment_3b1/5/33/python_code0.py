import pulp

# Data from JSON formatted input
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Parameters
C = data['C']
value = data['value']
size = data['size']
K = len(value)

# Create the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(value[k] * x[k] for k in range(K)), "TotalValue"

# Constraints
problem += pulp.lpSum(size[k] * x[k] for k in range(K)) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Output whether each item is included
isincluded = [x[k].varValue for k in range(K)]
print(f'Item inclusion: {isincluded}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')