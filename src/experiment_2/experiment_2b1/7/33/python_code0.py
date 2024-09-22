import pulp
import json

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extract values from the data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem variable
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Create decision variables
isincluded = pulp.LpVariable.dicts("item", range(K), cat='Binary')

# Objective function: Maximize total value
problem += pulp.lpSum([values[k] * isincluded[k] for k in range(K)]), "TotalValue"

# Constraint: Total size cannot exceed capacity
problem += pulp.lpSum([sizes[k] * isincluded[k] for k in range(K)]) <= C, "SizeConstraint"

# Solve the problem
problem.solve()

# Output results
isincluded_solution = [int(isincluded[k].varValue) for k in range(K)]
output = {"isincluded": isincluded_solution}
print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')