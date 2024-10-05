import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem
problem = pulp.LpProblem("Knapsack", pulp.LpMaximize)

# Decision Variables
K = len(data['value'])
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['value'][k] * x[k] for k in range(K))

# Constraint: Capacity
problem += pulp.lpSum(data['size'][k] * x[k] for k in range(K)) <= data['C']

# Solve the Problem
problem.solve()

# Output
isincluded = [int(x[k].varValue) for k in range(K)]
output = {"isincluded": isincluded}
print(output)

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')