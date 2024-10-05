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

# Extract data from the dictionary
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Create a linear programming problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Create decision variables for each process
x = [pulp.LpVariable(f'x_{l}', lowBound=0) for l in range(L)]

# Define the objective function
objective_terms = []
for l in range(L):
    revenue_contribution = pulp.lpSum(price[p] * output_matrix[l][p] for p in range(P))
    cost_contribution = cost[l] * pulp.lpSum(output_matrix[l][p] for p in range(P))
    objective_terms.append((revenue_contribution - cost_contribution) * x[l])

problem += pulp.lpSum(objective_terms), "Total Revenue"

# Add the constraints for crude oil allocation
for i in range(O):
    problem += pulp.lpSum(input_matrix[l][i] * x[l] for l in range(L)) <= allocated[i], f"Crude_Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')