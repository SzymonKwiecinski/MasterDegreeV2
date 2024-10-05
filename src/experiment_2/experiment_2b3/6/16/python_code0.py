import pulp

# Extracting the data from the provided JSON format
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: how many times each process should be executed
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective function: Maximize revenue
revenue = pulp.lpSum(
    (output_matrix[l][p] * price[p] - cost[l]) * execute[l]
    for l in range(L)
    for p in range(P)
)
problem += revenue

# Constraints: Crude allocations
for i in range(O):
    problem += pulp.lpSum(input_matrix[l][i] * execute[l] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Extract results
execute_values = [pulp.value(execute[l]) for l in range(L)]
revenue_value = pulp.value(problem.objective)

# Output format
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')