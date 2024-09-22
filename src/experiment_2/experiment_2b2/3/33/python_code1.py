import pulp

# Data input
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem definition
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
K = len(data['value'])
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['value'][k] * x[k] for k in range(K))

# Capacity constraint
problem += pulp.lpSum(data['size'][k] * x[k] for k in range(K)) <= data['C']

# Solve the problem
problem.solve()

# Output results
isincluded = [int(x[k].value()) for k in range(K)]
result = {"isincluded": isincluded}
print(result)

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')