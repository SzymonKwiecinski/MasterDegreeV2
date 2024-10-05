import pulp

# Data from JSON
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [
        [0.1, 0.9],
        [0.25, 0.75],
        [0.5, 0.5],
        [0.75, 0.25],
        [0.95, 0.05],
    ],
    'price': [5, 4, 3, 2, 1.5]
}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  # Number of alloys
M = len(target)  # Number of metals

# Define the Linear Programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum([prices[k] * x[k] for k in range(K)])

# Constraints
# Total weight constraint
problem += pulp.lpSum(x) == alloy_quant

# Metal composition constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) == target[m] * alloy_quant

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')