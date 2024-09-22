import pulp

# Data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "Total Value"

# Capacity constraint
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "Capacity Constraint"

# Solve the problem
problem.solve()

# Output results
isincluded = [x[k].varValue for k in range(K)]
print(f'Items included: {isincluded}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')