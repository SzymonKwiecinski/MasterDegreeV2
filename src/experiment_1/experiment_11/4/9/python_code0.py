import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
value = data['value']
size = data['size']

# Problem Definition
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Decision Variables
K = len(value)
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective Function
problem += pulp.lpSum(value[k] * x[k] for k in range(K)), "Total Value"

# Constraints
problem += pulp.lpSum(size[k] * x[k] for k in range(K)) <= C, "Total Size Constraint"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')