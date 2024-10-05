import pulp

# Problem data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extract data
C = data['C']
values = data['value']
sizes = data['size']
num_items = len(values)

# Define the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(num_items)]

# Objective function: maximize total value
problem += pulp.lpSum(values[k] * x[k] for k in range(num_items)), "Total Value"

# Constraint: total size should not exceed capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(num_items)) <= C, "Capacity Constraint"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "isincluded": [int(x[k].varValue) for k in range(num_items)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')