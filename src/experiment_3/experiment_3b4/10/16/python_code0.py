import pulp

# Data extracted from JSON
data = {
    'O': 2, 
    'P': 2, 
    'L': 3, 
    'Allocated': [8000, 5000],
    'Price': [38, 33], 
    'Input': [
        [3, 5],   # Inputs for process 1
        [1, 1],   # Inputs for process 2
        [5, 3]    # Inputs for process 3
    ], 
    'Output': [
        [4, 3],   # Outputs for process 1
        [1, 1],   # Outputs for process 2
        [3, 4]    # Outputs for process 3
    ], 
    'Cost': [51, 11, 40]
}

# Number of resource types, products, and processes
O = data['O']
P = data['P']
L = data['L']

# Extracting specific data
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{l}", lowBound=0, cat='Continuous') for l in range(L)]

# Objective function
objective = pulp.lpSum([
    pulp.lpSum([
        output_matrix[l][p] * x[l] for l in range(L)
    ]) * price[p] for p in range(P)
]) - pulp.lpSum([
    cost[l] * pulp.lpSum([
        output_matrix[l][p] * x[l] for p in range(P)
    ]) for l in range(L)
])

problem += objective

# Constraints
for i in range(O):
    constraint = pulp.lpSum([
        input_matrix[l][i] * x[l] for l in range(L)
    ]) <= allocated[i]
    problem += constraint

# Solve the problem
problem.solve()

# Output the results
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")