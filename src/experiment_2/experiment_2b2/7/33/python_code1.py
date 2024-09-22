import pulp

# Data input
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision Variables
isincluded = [pulp.LpVariable(f"isincluded_{k}", cat='Binary') for k in range(len(data['value']))]

# Objective
problem += pulp.lpSum(data['value'][k] * isincluded[k] for k in range(len(data['value'])))

# Constraint
problem += pulp.lpSum(data['size'][k] * isincluded[k] for k in range(len(data['size']))) <= data['C']

# Solve
problem.solve()

# Results
output = {
    "isincluded": [int(isincluded[k].varValue) for k in range(len(isincluded))]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')