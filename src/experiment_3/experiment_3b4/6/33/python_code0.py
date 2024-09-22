import pulp
import json

# Define the problem
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Load data
data = json.loads('{"C": 10, "value": [10, 20], "size": [8, 6]}')

# Parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

# Constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')