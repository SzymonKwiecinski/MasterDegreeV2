import pulp

# Data from the input
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [
        [0.1, 0.9],
        [0.25, 0.75],
        [0.5, 0.5],
        [0.75, 0.25],
        [0.95, 0.05]
    ],
    'price': [5, 4, 3, 2, 1.5]
}

# Problem definition
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables; x_k represents the quantity of alloy k to produce
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(len(data['price']))]

# Objective function: Minimize the total cost of the alloys
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(len(data['price'])))

# Constraint 1: Total quantity of alloys produced is exactly AlloyQuantity
problem += pulp.lpSum(x) == data['alloy_quant']

# Constraint 2: Quantity of each target component must be met or exceeded
for m in range(len(data['target'])):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(len(data['ratio']))) >= data['target'][m]

# Solving the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')