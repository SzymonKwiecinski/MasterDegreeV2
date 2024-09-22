import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extracting data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{k}", cat='Binary') for k in range(K)]

# Objective Function
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

# Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

# Solve
problem.solve()

# Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')