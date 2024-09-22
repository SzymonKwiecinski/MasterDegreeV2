import pulp

# Data
data = {
    'O': 2,
    'P': 2,
    'L': 3,
    'Allocated': [8000, 5000],
    'Price': [38, 33],
    'Input': [[3, 5], [1, 1], [5, 3]],
    'Output': [[4, 3], [1, 1], [3, 4]],
    'Cost': [51, 11, 40]
}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective Function
revenue = sum((price[p] * output_matrix[l][p] - cost[l]) * execute[l] for l in range(L) for p in range(P))
problem += revenue, "Total_Revenue"

# Constraints
for i in range(O):
    problem += sum(input_matrix[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Allocation_Constraint_{i}"

# Solve
problem.solve()

# Output
output = {
    "revenue": pulp.value(problem.objective),
    "execute": [pulp.value(execute[l]) for l in range(L)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')