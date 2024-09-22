import pulp

# Data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Create binary variables
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum([values[k] * isincluded[k] for k in range(K)]), "Total_Value"

# Constraints
problem += pulp.lpSum([sizes[k] * isincluded[k] for k in range(K)]) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Output results
isincluded_values = [int(isincluded[k].varValue) for k in range(K)]
print(f'Included items: {isincluded_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')