import pulp

# Data parsing
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33],
        'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
inputs = data['Input']
outputs = data['Output']
costs = data['Cost']

# Problem definition
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective function
revenue_terms = []
for l in range(L):
    output_revenue = sum(outputs[l][p] * price[p] for p in range(P))
    cost_term = costs[l]
    revenue_terms.append(execute[l] * (output_revenue - cost_term))

problem += pulp.lpSum(revenue_terms)

# Constraints
for i in range(O):
    problem += pulp.lpSum(inputs[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_Constraint_{i}"

# Solve problem
problem.solve()

# Extracting results
results = {
    "revenue": pulp.value(problem.objective),
    "execute": [pulp.value(execute[l]) for l in range(L)]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')