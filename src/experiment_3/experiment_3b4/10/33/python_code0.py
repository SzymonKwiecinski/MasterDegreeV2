import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
values = data['value']
sizes = data['size']
capacity = data['C']
num_items = len(values)

# Problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision Variables
isincluded = [pulp.LpVariable(f'isincluded_{k}', cat='Binary') for k in range(num_items)]

# Objective Function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(num_items)), "Total Value"

# Constraints
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(num_items)) <= capacity, "Capacity Constraint"

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')