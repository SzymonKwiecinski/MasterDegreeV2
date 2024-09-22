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
L = data['L']
O = data['O']
P = data['P']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']

# Problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective Function
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_matrix[l][p] * x[l] for l in range(L)) for p in range(P))
problem += revenue

# Constraints

# Crude Oil Constraints
for i in range(O):
    problem += pulp.lpSum(input_matrix[l][i] * x[l] for l in range(L)) <= allocated[i]

# Solve the Problem
problem.solve()

# Output the results
print("Optimization Results:")
for l in range(L):
    print(f"Process {l + 1} should be executed {x[l].varValue} times.")

print(f"Total revenue (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")