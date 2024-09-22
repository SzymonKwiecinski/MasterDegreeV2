import pulp

# Extracting provided data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
inputs = data['Input']
output = data['Output']
cost = data['Cost']

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: times each process is executed
execute = [pulp.LpVariable(f"x_{l}", lowBound=0) for l in range(L)]

# Objective function: Maximize total revenue
revenue = pulp.lpSum(
    (pulp.lpSum(output[l][p] * price[p] for p in range(P)) - cost[l]) * execute[l]
    for l in range(L)
)
problem += revenue

# Constraint: Crude oil allocation
for i in range(O):
    problem += pulp.lpSum(inputs[l][i] * execute[l] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Prepare the output
revenue_result = pulp.value(revenue)
execute_result = [pulp.value(execute[l]) for l in range(L)]

output = {
    "revenue": revenue_result,
    "execute": execute_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')