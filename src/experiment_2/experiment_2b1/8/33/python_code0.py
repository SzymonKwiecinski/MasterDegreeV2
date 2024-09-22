import pulp
import json

# Data input
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Create binary variables for each item
x = pulp.LpVariable.dicts("item", range(K), cat='Binary')

# Objective function: Maximize the total value
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "TotalValue"

# Capacity constraint
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "Capacity"

# Solve the problem
problem.solve()

# Output the solution
isincluded = [int(x[k].varValue) for k in range(K)]
output = {"isincluded": isincluded}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')