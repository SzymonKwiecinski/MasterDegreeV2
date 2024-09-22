import pulp

# Data from the provided JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Unpack data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem variable
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Decision Variables
isincluded = [pulp.LpVariable(f'isincluded_{k}', cat='Binary') for k in range(K)]

# Objective Function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K)), "Objective"

# Constraints
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C, "Capacity Constraint"

# Solve the problem
problem.solve()

# Collect the solution
solution = {"isincluded": [pulp.value(isincluded[k]) for k in range(K)]}

# Print the solution
print(solution)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')