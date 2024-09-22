import pulp
import json

# Input data in JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extracting values from the data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create a problem variable
problem = pulp.LpProblem('KnapsackProblem', pulp.LpMaximize)

# Create binary variables for each item
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

# Objective function: Maximize total value of packed items
problem += pulp.lpSum([values[k] * isincluded[k] for k in range(K)])

# Constraint: The total size of items cannot exceed the capacity
problem += pulp.lpSum([sizes[k] * isincluded[k] for k in range(K)]) <= C

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "isincluded": [int(isincluded[k].varValue) for k in range(K)]
}

# Print the results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')