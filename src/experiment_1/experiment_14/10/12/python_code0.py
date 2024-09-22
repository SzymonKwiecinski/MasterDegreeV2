import pulp

# Data provided in JSON format
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

# Extract data details
alloy_quantity = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']
K = len(prices)
M = len(targets)

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision Variables
x_vars = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum([prices[k] * x_vars[k] for k in range(K)])

# Constraints
# 1. Total quantity constraint
problem += pulp.lpSum([x_vars[k] for k in range(K)]) == alloy_quantity

# 2. Target component constraints
for m in range(M):
    problem += pulp.lpSum([ratios[k][m] * x_vars[k] for k in range(K)]) >= targets[m]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')