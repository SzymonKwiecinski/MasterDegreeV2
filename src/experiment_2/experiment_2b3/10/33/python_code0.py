import pulp

# Data from the problem
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Unpack data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize the total value
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

# Constraint: Total size must not exceed the capacity C
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

# Solve the problem
problem.solve()

# Extract the solution
isincluded = [int(x[k].varValue) for k in range(K)]

# Output the solution
output = {
    "isincluded": isincluded
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')