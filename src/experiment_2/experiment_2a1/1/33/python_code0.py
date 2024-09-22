import pulp
import json

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extract data from the input
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem variable
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Create binary decision variables for each item
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective Function: Maximize total value
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

# Constraint: Total size must not exceed capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Output results
isincluded = [int(x[k].varValue) for k in range(K)]
output = {
    "isincluded": isincluded
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')