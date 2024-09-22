import pulp

# Load the data
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

# Unpack data
alloy_quant = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)
M = len(targets)

# Create a problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
amounts = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * amounts[k] for k in range(K))

# Constraints for each metal target
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * amounts[k] for k in range(K)) == targets[m]

# Solve the problem
problem.solve()

# Output format
solution = {"amount": [pulp.value(amounts[k]) for k in range(K)]}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')