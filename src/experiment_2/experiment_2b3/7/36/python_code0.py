import pulp

# Parse input data
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}
alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

# Number of different alloys and metals
K = len(ratios)
M = len(target)

# Define LP problem
problem = pulp.LpProblem('Alloy_Blending', pulp.LpMinimize)

# Define variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum([prices[k] * amount[k] for k in range(K)])

# Constraints for achieving target metal content
for m in range(M):
    problem += pulp.lpSum([ratios[k][m] * amount[k] for k in range(K)]) == target[m]

# Total alloy amount constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant

# Solve the problem
problem.solve()

# Extract results
result_amount = [pulp.value(amount[k]) for k in range(K)]

# Output result
output = {
    "amount": result_amount
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')