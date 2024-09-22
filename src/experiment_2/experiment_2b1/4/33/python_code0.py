import pulp
import json

# Given data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Define the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Define decision variables
K = len(data['value'])
isincluded = pulp.LpVariable.dicts("item", range(K), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['value'][k] * isincluded[k] for k in range(K)), "TotalValue"

# Constraints
problem += pulp.lpSum(data['size'][k] * isincluded[k] for k in range(K)) <= data['C'], "CapacityConstraint"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "isincluded": [int(isincluded[k].varValue) for k in range(K)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')