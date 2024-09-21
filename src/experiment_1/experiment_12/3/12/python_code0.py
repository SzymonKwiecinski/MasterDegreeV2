import pulp

# Extract data from JSON
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

alloy_quantity = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # Number of alloys
M = len(target)  # Number of components

# Define the optimization problem
problem = pulp.LpProblem("Alloy_Production_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints

# Total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Quantity_Constraint"

# Quantity of each target component
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) >= target[m], f"Component_{m}_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')