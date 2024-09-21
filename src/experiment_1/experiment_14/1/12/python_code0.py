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
        [0.95, 0.05]
    ],
    'price': [5, 4, 3, 2, 1.5]
}

# Extract data
alloy_quantity = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

# Number of alloys (K) and components (M)
K = len(prices)
M = len(targets)

# Define the problem
problem = pulp.LpProblem("Alloy_Production_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total Cost"

# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Quantity_Constraint"

# Constraint 2: Target component quantity constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= targets[m], f"Target_Component_{m}_Constraint"

# Solve the problem
problem.solve()

# Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for k in range(K):
    print(f'x_{k}: {x[k].varValue}')