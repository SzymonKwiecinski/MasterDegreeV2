import pulp

# Data from the problem
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Initialize problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables for the number of times each process is executed
execute = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective Function: Maximize Revenue
problem += pulp.lpSum([(output_matrix[l][p] * price[p] - cost[l]) * execute[l] for l in range(L) for p in range(P)])

# Constraints for allocated crudes
for i in range(O):
    problem += pulp.lpSum([input_matrix[l][i] * execute[l] for l in range(L)]) <= allocated[i]

# Solve the problem
problem.solve()

# Prepare the output
revenue = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

# Print the results
print({
    "revenue": revenue,
    "execute": execute_values
})
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')