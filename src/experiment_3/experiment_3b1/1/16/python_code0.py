import pulp

# Data from JSON
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

# Sets
O = data['O']  # Number of crude oil types
P = data['P']  # Number of products
L = data['L']  # Number of production processes

# Parameters
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, L + 1), lowBound=0, cat='Continuous')

# Create the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Objective Function
revenue_expr = pulp.lpSum(price[p-1] * pulp.lpSum(output_data[l-1][p-1] * x[l] for l in range(1, L + 1)) for p in range(1, P + 1))
problem += revenue_expr, "Total_Revenue"

# Constraints
for i in range(1, O + 1):
    problem += pulp.lpSum(input_data[l-1][i-1] * x[l] for l in range(1, L + 1)) <= allocated[i-1], f"Crude_Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the number of times each process should be executed
for l in range(1, L + 1):
    print(f'Process {l} should be executed {x[l].varValue} times.')