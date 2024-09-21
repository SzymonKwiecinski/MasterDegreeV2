import pulp

# Data
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

alloy_quant = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

num_alloys = len(prices)
num_components = len(targets)

# Problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(num_alloys)]

# Objective Function
problem += pulp.lpSum(prices[k] * x[k] for k in range(num_alloys))

# Constraints
# Total quantity of alloys
problem += pulp.lpSum(x) == alloy_quant

# Target components must be met or exceeded
for m in range(num_components):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(num_alloys)) >= targets[m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')