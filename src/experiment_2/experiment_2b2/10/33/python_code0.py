import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Variables
isincluded = [pulp.LpVariable(f"isincluded_{k}", cat='Binary') for k in range(K)]

# Objective
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K)), "Total Value of Packed Items"

# Constraints
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C, "Capacity Constraint"

# Solve
problem.solve()

# Output
output = {
    "isincluded": [int(isincluded[k].varValue) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')