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

# Unpack data
alloy_quantity = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

# Number of alloys and components
K = len(prices)    # Number of different alloys
M = len(targets)   # Number of target components

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Define the decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraint 1: Total quantity of alloys
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Alloy_Quantity"

# Constraint 2: Target component constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= targets[m], f"Target_Component_{m}"

# Solve the problem
problem.solve()

# Output the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for k in range(K):
    print(f'Quantity of Alloy {k}: {pulp.value(x[k])}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')