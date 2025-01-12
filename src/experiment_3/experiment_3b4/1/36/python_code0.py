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

alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
K = len(price)
M = len(target)

# Problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

# Objective
problem += pulp.lpSum(price[k] * x[k] for k in range(K))

# Total weight constraint
problem += pulp.lpSum([x[k] for k in range(K)]) == alloy_quant

# Metal proportion requirements
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m] * alloy_quant

# Solve
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')