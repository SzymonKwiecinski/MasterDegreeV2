import pulp

# Data input
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
capacity = data['C']
values = data['value']
sizes = data['size']
num_items = len(values)

# Initialize the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', cat='Binary') for i in range(num_items)]

# Objective function
problem += pulp.lpSum(values[i] * x[i] for i in range(num_items))

# Constraint: Capacity of the knapsack
problem += pulp.lpSum(sizes[i] * x[i] for i in range(num_items)) <= capacity

# Solve the problem
problem.solve()

# Retrieve the solution
isincluded = [int(x[i].varValue) for i in range(num_items)]

# Output format
output = {"isincluded": isincluded}
print(output)

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')