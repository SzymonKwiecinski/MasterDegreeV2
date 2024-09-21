import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Number of items
K = len(values)

# Initialize the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

# Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Size_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')