import pulp

# Define the linear programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Data from JSON
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

# Parameters
K = len(data['price'])  # Number of alloys
M = len(data['target'])  # Number of metals
alloy_quant = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

# Decision Variables
amounts = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(prices[k] * amounts[k] for k in range(K))

# Constraints
# Total quantity constraint
problem += pulp.lpSum(amounts[k] for k in range(K)) == alloy_quant

# Metal composition constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * amounts[k] for k in range(K)) == targets[m]

# Solve the problem
problem.solve()

# Print the results
amounts_solution = [pulp.value(x) for x in amounts]
print(f'Amounts of each alloy to purchase: {amounts_solution}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')