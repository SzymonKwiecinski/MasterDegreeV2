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

# Extracting data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_ = data['Input']
output = data['Output']
cost = data['Cost']

# Initialize LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective function
revenue = pulp.lpSum([(price[p] * output[l][p] - cost[l]) * execute[l] for l in range(L) for p in range(P)])
problem += revenue

# Constraints
for i in range(O):
    problem += pulp.lpSum([input_[l][i] * execute[l] for l in range(L)]) <= allocated[i]

# Solve the problem
problem.solve()

# Collect results
execute_result = [pulp.value(execute[l]) for l in range(L)]
revenue_result = pulp.value(problem.objective)

# Output format
output = {
    "revenue": revenue_result,
    "execute": execute_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')