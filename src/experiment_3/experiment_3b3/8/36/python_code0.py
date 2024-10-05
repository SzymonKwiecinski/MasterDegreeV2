import pulp

# Data from JSON
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

# Number of alloys and metals
K = len(prices)
M = len(target)

# Problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * amount[k] for k in range(K))

# Constraints
# Total amount of alloy constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant

# Metal requirements constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * amount[k] for k in range(K)) >= target[m]

# Solve the problem
problem.solve()

# Output the results
amount_values = [pulp.value(amount[k]) for k in range(K)]
print(f'Amount of each alloy to purchase: {amount_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')