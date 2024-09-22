import pulp

# Data provided
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extract data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
isincluded = [pulp.LpVariable(f"isincluded_{k}", cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K)), "Total_Value"

# Constraints
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Output which items are included
output = {'isincluded': [pulp.value(isincluded[k]) for k in range(K)]}
print(f'Output: {output}')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')