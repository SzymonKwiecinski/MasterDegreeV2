import pulp

# Data provided
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

# Number of metals K
K = len(data['price'])

# Number of target metals M
M = len(data['target'])

# Problem
problem = pulp.LpProblem("Metal_Alloy_Optimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K))

# Total weight constraint
problem += pulp.lpSum(x[k] for k in range(K)) == data['alloy_quant']

# Metal composition constraints
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(K)) == data['target'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')