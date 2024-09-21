import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

# Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

# Solve the problem
problem.solve()

# Output the results
print(f"Status: {pulp.LpStatus[problem.status]}")
for k in range(K):
    print(f"x_{k} = {pulp.value(x[k])}")

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')