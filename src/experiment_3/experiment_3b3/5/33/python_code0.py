import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
capacity = data['C']
values = data['value']
sizes = data['size']
num_items = len(values)

# Problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(num_items)]

# Objective Function
problem += pulp.lpSum(values[k] * x[k] for k in range(num_items)), "Total Value"

# Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(num_items)) <= capacity, "Total Size"

# Solve
problem.solve()

# Output
output = [pulp.value(x[k]) for k in range(num_items)]
print("Included in knapsack:", output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')