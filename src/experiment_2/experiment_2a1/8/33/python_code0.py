import pulp
import json

# Given data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem definition
problem = pulp.LpProblem("Knapsack Problem", pulp.LpMaximize)

# Variables
K = len(data['value'])
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(data['value'][k] * isincluded[k] for k in range(K))

# Constraints
problem += pulp.lpSum(data['size'][k] * isincluded[k] for k in range(K)) <= data['C']

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "isincluded": [int(isincluded[k].value()) for k in range(K)]
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')