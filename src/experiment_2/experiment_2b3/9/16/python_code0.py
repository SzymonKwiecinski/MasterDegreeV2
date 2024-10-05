import pulp

# Parse the JSON input data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: How many times each process is executed
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Maximize Revenue
revenue_terms = [
    pulp.lpSum(output_matrix[l][p] * price[p] for p in range(P)) * execute[l]
    - cost[l] * execute[l]
    for l in range(L)
]
problem += pulp.lpSum(revenue_terms)

# Constraints: Crude oil allocation
for i in range(O):
    problem += (
        pulp.lpSum(input_matrix[l][i] * execute[l] for l in range(L)) <= allocated[i],
        f"Crude_Allocation_{i}"
    )

# Solve the problem
problem.solve()

# Collect the results
revenue = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

# Output results in the specified format
output = {
    "revenue": revenue,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')