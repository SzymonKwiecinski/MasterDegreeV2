import pulp
import json

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem definition
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
K = len(data['value'])
isincluded = [pulp.LpVariable(f'item_{k}', cat='Binary') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['value'][k] * isincluded[k] for k in range(K)), "Total_Value"

# Constraints
problem += pulp.lpSum(data['size'][k] * isincluded[k] for k in range(K)) <= data['C'], "Capacity_Constraint"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "isincluded": [int(isincluded[k].varValue) for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print output
print(output)