import pulp

# Parsing the provided data
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

# Extracting relevant variables from the data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
inputs = data['Input']
outputs = data['Output']
costs = data['Cost']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: number of times each process is executed
execute_vars = [pulp.LpVariable(f"execute_{l}", lowBound=0, cat='Continuous') for l in range(L)]

# Objective function: maximize revenue
# Revenue from products
revenue = pulp.lpSum([outputs[l][p] * price[p] * execute_vars[l] for l in range(L) for p in range(P)])
# Costs from processes
process_cost = pulp.lpSum([costs[l] * execute_vars[l] for l in range(L)])
# Maximize revenue (revenue - costs)
problem += revenue - process_cost

# Constraints: Ensure the allocated crude limits are not exceeded
for i in range(O):
    problem += pulp.lpSum([inputs[l][i] * execute_vars[l] for l in range(L)]) <= allocated[i]

# Solve the problem
problem.solve()

# Prepare the output
revenue = pulp.value(problem.objective)
execute = [pulp.value(execute_vars[l]) for l in range(L)]

result = {
    "revenue": revenue,
    "execute": execute
}

# Print the results
print(result)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")