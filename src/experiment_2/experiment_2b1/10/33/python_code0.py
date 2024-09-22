import pulp
import json

data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Define the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Define decision variables
K = len(values)
x = pulp.LpVariable.dicts("item", range(K), cat='Binary')

# Objective function: Maximize total value
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "TotalValue"

# Capacity constraint: Total size should not exceed C
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Prepare the output
isincluded = [int(x[k].varValue) for k in range(K)]
output = {"isincluded": isincluded}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')