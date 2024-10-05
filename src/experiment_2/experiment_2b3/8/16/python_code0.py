import pulp

# Data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_oil = data['Input']
output_product = data['Output']
cost = data['Cost']

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective
revenue = pulp.lpSum([(pulp.lpSum([output_product[l][p] * price[p] for p in range(P)]) - cost[l]) * execute[l] for l in range(L)])
problem += revenue

# Constraints
for i in range(O):
    problem += pulp.lpSum([input_oil[l][i] * execute[l] for l in range(L)]) <= allocated[i]

# Solve
problem.solve()

# Outputs
revenue_value = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')