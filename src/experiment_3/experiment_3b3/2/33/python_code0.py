import pulp

# Parse the data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create a problem instance
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Define decision variables
isincluded = [pulp.LpVariable(f'isincluded_{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K)), "Total Value"

# Constraint: Total size must not exceed capacity
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C, "Capacity"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')