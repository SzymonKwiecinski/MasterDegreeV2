import pulp

# Data input
data = {
    'C': 10,
    'value': [10, 20],
    'size': [8, 6]
}

# Extracting data
capacity = data['C']
values = data['value']
sizes = data['size']
num_items = len(values)

# Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', cat='Binary') for i in range(num_items)]

# Objective function
problem += pulp.lpSum(values[i] * x[i] for i in range(num_items)), "Total Value"

# Constraint: Total size cannot exceed the capacity
problem += pulp.lpSum(sizes[i] * x[i] for i in range(num_items)) <= capacity, "Capacity Constraint"

# Solve the problem
problem.solve()

# Output results
isincluded = [int(x[i].varValue) for i in range(num_items)]
output = {"isincluded": isincluded}

# Print output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')