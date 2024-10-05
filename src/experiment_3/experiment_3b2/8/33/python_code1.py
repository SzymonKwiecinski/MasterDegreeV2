import pulp

# Data from JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Number of items
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)  # Changed the name to remove spaces

# Create binary variables for each item
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function: Maximize total value
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "Total_Value"  # Changed the name to remove spaces

# Constraint: Total size must not exceed capacity
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "Size_Limit"  # Changed the name to remove spaces

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')