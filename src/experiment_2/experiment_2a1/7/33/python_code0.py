import pulp
import json

# Given data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem setup
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Variables
K = len(data['value'])
isincluded = [pulp.LpVariable(f'item_{k}', cat='Binary') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['value'][k] * isincluded[k] for k in range(K)), "TotalValue"

# Capacity Constraint
problem += pulp.lpSum(data['size'][k] * isincluded[k] for k in range(K)) <= data['C'], "CapacityConstraint"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "isincluded": [int(isincluded[k].varValue) for k in range(K)]
}

# Print output and objective value
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')