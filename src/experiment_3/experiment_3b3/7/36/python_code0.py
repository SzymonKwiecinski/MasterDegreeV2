import pulp

# Data provided
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Extract parameters
A = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
M = len(target)
K = len(price)

# Initialize the LP problem
problem = pulp.LpProblem("Alloy_Production_Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K))

# Constraint: Total amount of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == A, "Total_Alloy_Quantity"

# Constraints: Metal composition requirements
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"Metal_Composition_{m+1}"

# Solve the problem
problem.solve()

# Output results
amounts = {f'x_{k}': pulp.value(x[k]) for k in range(K)}
print("The amounts of each alloy to purchase:")
for k in amounts:
    print(f'{k}: {amounts[k]}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')