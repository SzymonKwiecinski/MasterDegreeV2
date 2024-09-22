import pulp

# Given data
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

# Extracting data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_l_i = data['Input']
output_l_p = data['Output']
cost = data['Cost']

# Create a LP maximization problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute_vars = [pulp.LpVariable(f'Execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Maximize Revenue
revenue = sum((sum(output_l_p[l][p] * price[p] for p in range(P)) - cost[l]) * execute_vars[l] for l in range(L))
problem += revenue

# Constraints: Crude oil allocation
for i in range(O):
    problem += sum(input_l_i[l][i] * execute_vars[l] for l in range(L)) <= allocated[i]

# Solving the problem
problem.solve()

# Collecting results
revenue_value = pulp.value(problem.objective)
execute_values = [pulp.value(execute_vars[l]) for l in range(L)]

# Output format
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')