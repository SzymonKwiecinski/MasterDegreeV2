import pulp

# Data from input
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

M = len(target)
K = len(prices)

# Define the problem
problem = pulp.LpProblem("AlloyProduction", pulp.LpMinimize)

# Define decision variables
amounts = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum([prices[k] * amounts[k] for k in range(K)])

# Constraints for each metal
for m in range(M):
    problem += pulp.lpSum([ratios[k][m] * amounts[k] for k in range(K)]) == target[m]

# Solve the problem
problem.solve()

# Prepare the output
amount_output = [amounts[k].varValue for k in range(K)]

output = {"amount": amount_output}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')