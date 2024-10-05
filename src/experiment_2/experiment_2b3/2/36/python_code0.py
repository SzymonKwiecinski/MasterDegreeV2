import pulp

# Input data
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

M = len(target)
K = len(prices)

# Define the LP problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Define decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum([prices[k] * amount[k] for k in range(K)])

# Constraints to meet target metal requirements
for m in range(M):
    problem += pulp.lpSum([ratios[k][m] * amount[k] for k in range(K)]) == target[m]

# Solve the problem
problem.solve()

# Output results
output = {"amount": [pulp.value(amount[k]) for k in range(K)]}
print(output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")