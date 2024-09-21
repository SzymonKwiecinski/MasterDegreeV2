import pulp

# Data from the provided JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the LP problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total Value"

# Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Total Size Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')