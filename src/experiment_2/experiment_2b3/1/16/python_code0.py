import pulp

# Data input
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

# Unpack data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
inputs = data['Input']
outputs = data['Output']
costs = data['Cost']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective function
revenue_terms = []
for l in range(L):
    process_revenue = sum(outputs[l][p] * price[p] for p in range(P)) - costs[l]
    revenue_terms.append(process_revenue * execute[l])

problem += pulp.lpSum(revenue_terms), "Total_Revenue"

# Constraints
# Crude oil usage constraints
for i in range(O):
    problem += pulp.lpSum(inputs[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_{i}_Usage"

# Solve the problem
problem.solve()

# Gather results
revenue = pulp.value(problem.objective)
execute_values = [execute[l].varValue for l in range(L)]

# Output
output = {
    "revenue": revenue,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')