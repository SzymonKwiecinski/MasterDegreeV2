import pulp
import json

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the LP problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("item", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

# Constraints
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