import pulp

# Extracting data from JSON
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

# Number of metals and alloys
M = len(target)
K = len(ratios)

# Problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum([prices[k] * amount[k] for k in range(K)])

# Constraints
# Ensure total amount of the final alloy is alloy_quant
problem += pulp.lpSum(amount) == alloy_quant

# Ensure target ratios of individual metals
for m in range(M):
    problem += pulp.lpSum([ratios[k][m] * amount[k] for k in range(K)]) == target[m]

# Solve the problem
problem.solve()

# Extracting results
result = {"amount": [pulp.value(amount[k]) for k in range(K)]}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')