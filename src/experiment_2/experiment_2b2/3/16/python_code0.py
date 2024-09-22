import pulp

# Given data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 
        'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 
        'Cost': [51, 11, 40]}

# Extract data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Create maximization problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: number of times each process is executed
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Total revenue - Total cost
revenue = pulp.lpSum([execute[l] * (pulp.lpSum(output_matrix[l][p] * price[p] for p in range(P)) - cost[l]) for l in range(L)])
problem += revenue

# Constraints: Limited crude oil allocation
for i in range(O):
    problem += (pulp.lpSum(execute[l] * input_matrix[l][i] for l in range(L)) <= allocated[i])

# Solve problem
problem.solve()

# Extract results
execute_values = [pulp.value(execute[l]) for l in range(L)]
revenue_value = pulp.value(problem.objective)

# Print results
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')