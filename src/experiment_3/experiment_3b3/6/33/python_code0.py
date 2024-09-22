import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Problem
problem = pulp.LpProblem("Knapsack", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x{k}', cat='Binary') for k in range(K)] 

# Objective Function
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

# Constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

# Solve
problem.solve()

# Results
isincluded = [pulp.value(x[k]) for k in range(K)]
print(f'Included items: {isincluded}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')