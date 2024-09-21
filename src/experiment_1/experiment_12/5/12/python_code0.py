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

# Parameters
alloy_quantity = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)
M = len(targets)

# Problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total Cost"

# Constraints
# 1. Total quantity of alloys
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Quantity"

# 2. Target component constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= targets[m], f"Target_{m+1}"

# Solving the problem
problem.solve()

# Printing the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')