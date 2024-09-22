import pulp
import json

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Extract values from the input data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create a linear programming problem
problem = pulp.LpProblem("Knapsack", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

# Objective function: Maximize total value
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total Value"

# Constraint: The total size should not exceed the capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity Constraint"

# Solve the problem
problem.solve()

# Collect the results
isincluded = [int(x[k].varValue) for k in range(K)]

# Output the results
output = {
    "isincluded": isincluded
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')