import pulp

# Read input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Number of items
K = len(data['value'])

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", cat="Binary") for k in range(K)]

# Objective function: Maximize the total value of the packed items
problem += pulp.lpSum(data['value'][k] * x[k] for k in range(K))

# Constraint: Total size should not exceed the capacity C
problem += pulp.lpSum(data['size'][k] * x[k] for k in range(K)) <= data['C']

# Solve the problem
problem.solve()

# Extract results
isincluded = [pulp.value(x[k]) for k in range(K)]

# Prepare output in the specified format
output = {
    "isincluded": isincluded
}

# Print the output
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')