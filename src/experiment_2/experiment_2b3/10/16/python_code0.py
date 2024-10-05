import pulp

# Data from the input
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Parameters
allocated = data['Allocated']
price = data['Price']
input_amount = data['Input']
output_amount = data['Output']
cost = data['Cost']

O = data['O']
P = data['P']
L = data['L']

# Problem definition
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective function
profit = []
for l in range(L):
    revenue_from_l = sum(output_amount[l][p] * price[p] for p in range(P))
    cost_of_l = cost[l]
    profit.append((revenue_from_l - cost_of_l) * execute[l])

problem += pulp.lpSum(profit)

# Constraints
# Crude oil constraints
for i in range(O):
    problem += pulp.lpSum(input_amount[l][i] * execute[l] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Output the results
revenue = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

output = {
    "revenue": revenue,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')