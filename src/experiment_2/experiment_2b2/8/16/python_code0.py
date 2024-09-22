import pulp

# Parsing the input data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

num_o = data['O']
num_p = data['P']
num_l = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Define the linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: x_l = number of times process l is executed
x = [pulp.LpVariable(f"x_{l}", lowBound=0, cat='Continuous') for l in range(num_l)]

# Objective function: Maximize the total revenue
revenue_terms = [(output_matrix[l][p] * price[p] - cost[l]) * x[l] for l in range(num_l) for p in range(num_p)]
problem += pulp.lpSum(revenue_terms)

# Constraints: Allocated resources for each crude oil type
for i in range(num_o):
    problem += pulp.lpSum([input_matrix[l][i] * x[l] for l in range(num_l)]) <= allocated[i]

# Solve the problem
problem.solve()

# Prepare the output
revenue = pulp.value(problem.objective)
execute = [pulp.value(x[l]) for l in range(num_l)]

# Output
output = {
    "revenue": revenue,
    "execute": execute
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')