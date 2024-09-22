import pulp

# Data extraction from JSON
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

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
inputs = data['Input']
outputs = data['Output']
cost = data['Cost']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{l}", lowBound=0, cat='Continuous') for l in range(L)]

# Objective function
revenue_components = []
for l in range(L):
    process_revenue = sum(outputs[l][p] * price[p] for p in range(P)) - cost[l]
    revenue_components.append(process_revenue * x[l])
problem += pulp.lpSum(revenue_components)

# Constraints
# Crude Oil Allocation Constraints
for i in range(O):
    problem += pulp.lpSum(inputs[l][i] * x[l] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Print the optimal objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')