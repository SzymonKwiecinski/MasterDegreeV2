import pulp

# Load the data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Create the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Number of items
K = len(data["value"])

# Decision variables
is_included = [pulp.LpVariable(f"is_included_{k}", cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(data["value"][k] * is_included[k] for k in range(K)), "Total Value"

# Constraint: total size cannot exceed capacity
problem += pulp.lpSum(data["size"][k] * is_included[k] for k in range(K)) <= data["C"], "Capacity"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "isincluded": [int(is_included[k].varValue) for k in range(K)]
}

# Print output
print(output)

# Print objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')