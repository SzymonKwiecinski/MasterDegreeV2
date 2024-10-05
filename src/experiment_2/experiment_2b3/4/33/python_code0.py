import pulp

# Load data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
isincluded = [pulp.LpVariable(f"x{k}", cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K))

# Constraint: Total size should not exceed capacity
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C

# Solve the problem
problem.solve()

# Prepare the solution
solution = {
    "isincluded": [int(isincluded[k].varValue) for k in range(K)]
}

print(solution)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')