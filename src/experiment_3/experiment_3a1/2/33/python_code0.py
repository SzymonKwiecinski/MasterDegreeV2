import pulp

# Given data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create a linear programming problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Define binary variables
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

# Objective Function
problem += pulp.lpSum([values[k] * isincluded[k] for k in range(K)])

# Constraints
problem += pulp.lpSum([sizes[k] * isincluded[k] for k in range(K)]) <= C

# Solve the problem
problem.solve()

# Output results
included_items = [k for k in range(K) if pulp.value(isincluded[k]) == 1]
print(f'Included items: {included_items}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')