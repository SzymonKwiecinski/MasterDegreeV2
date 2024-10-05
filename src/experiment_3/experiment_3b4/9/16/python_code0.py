import pulp

# Data
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

# Variables
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
costs = data['Cost']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0) for l in range(L)]

# Objective function
objective = pulp.lpSum([pulp.lpSum(output_matrix[l][p] * price[p] * x[l] for p in range(P)) - costs[l] * x[l] for l in range(L)])
problem += objective

# Constraints
for i in range(O):
    problem += pulp.lpSum(input_matrix[l][i] * x[l] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')