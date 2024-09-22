import pulp

# Data from input
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Number of items
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Create binary variables for each item
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize total value
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "Total_Value"

# Constraint: Total size must not exceed the capacity
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Get the included items
isincluded = [int(x[k].varValue) for k in range(K)]

# Prepare output
output = {
    "isincluded": isincluded
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')