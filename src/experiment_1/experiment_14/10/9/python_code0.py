import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Variables
K = len(data['value'])  # Number of items
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['value'][k] * x[k] for k in range(K)), "Total Value"

# Constraints
problem += pulp.lpSum(data['size'][k] * x[k] for k in range(K)) <= data['C'], "Capacity Constraint"

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')