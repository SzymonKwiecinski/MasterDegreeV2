import pulp

# Define the data
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

# Extract data from dictionary for convenience
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
inputs = data['Input']
outputs = data['Output']
cost = data['Cost']

# Initialize LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables for each process
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Maximize revenue
# Revenue from selling products minus cost of production processes
revenue = pulp.lpSum((price[p] * outputs[l][p] - cost[l]) * execute[l] for l in range(L) for p in range(P))
problem += revenue

# Constraints: Crude oil allocation
for i in range(O):
    problem += pulp.lpSum(inputs[l][i] * execute[l] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Extract solution
execute_values = [pulp.value(execute[l]) for l in range(L)]
revenue_value = pulp.value(problem.objective)

# Format the output
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')