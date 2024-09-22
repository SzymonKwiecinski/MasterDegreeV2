import pulp
import json

# Input data in JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("item", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

# Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity"

# Solve the problem
problem.solve()

# Output
isincluded = [int(x[k].varValue) for k in range(K)]
output = {
    "isincluded": isincluded
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')