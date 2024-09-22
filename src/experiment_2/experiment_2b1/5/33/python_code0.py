import pulp
import json

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem variables
C = data['C']
values = data['value']
sizes = data['size']
num_items = len(values)

# Create the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("item", range(num_items), cat='Binary')

# Objective function
problem += pulp.lpSum([values[k] * x[k] for k in range(num_items)]), "TotalValue"

# Constraints
problem += pulp.lpSum([sizes[k] * x[k] for k in range(num_items)]) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Output result
isincluded = [int(x[k].varValue) for k in range(num_items)]
output = {
    "isincluded": isincluded
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')