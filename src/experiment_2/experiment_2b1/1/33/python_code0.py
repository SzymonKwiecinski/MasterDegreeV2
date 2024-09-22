import pulp
import json

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Define binary variables
x = pulp.LpVariable.dicts("item", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "TotalValue"

# Capacity constraint
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Prepare the output
isincluded = [int(x[k].varValue) for k in range(K)]

# Print the results
result = {
    "isincluded": isincluded
}
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')