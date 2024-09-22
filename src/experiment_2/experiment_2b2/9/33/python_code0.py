import pulp

# Parse the input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
capacity = data['C']
values = data['value']
sizes = data['size']
num_items = len(values)

# Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(num_items)]

# Define the objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(num_items))

# Define the constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(num_items)) <= capacity

# Solve the problem
problem.solve()

# Extract the solution
isincluded = [int(x[k].varValue) for k in range(num_items)]

# Print the output
output = {
    "isincluded": isincluded
}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')