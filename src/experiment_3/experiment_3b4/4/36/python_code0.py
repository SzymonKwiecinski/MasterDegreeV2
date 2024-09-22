import pulp

# Data
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Problem Definition
problem = pulp.LpProblem("Alloy_Mixture_Minimization", pulp.LpMinimize)

# Decision Variables
K = len(data['price'])
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

# Objective Function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)])

# Constraints
# Total Alloy Quantity Constraint
problem += pulp.lpSum(x) == data['alloy_quant']

# Target Content Constraints
M = len(data['target'])
for m in range(M):
    problem += pulp.lpSum([data['ratio'][k][m] * x[k] for k in range(K)]) == data['target'][m] * data['alloy_quant']

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')