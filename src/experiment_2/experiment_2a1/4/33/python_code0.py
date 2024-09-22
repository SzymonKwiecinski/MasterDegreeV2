import pulp
import json

# Given data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Create decision variables
x = pulp.LpVariable.dicts('x', range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

# Constraint: total size must not exceed capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Prepare output
isincluded = [int(x[k].varValue) for k in range(K)]
output = {"isincluded": isincluded}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')