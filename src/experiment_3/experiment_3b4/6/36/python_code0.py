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

# Define the problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision variables
K = len(data['price'])
x = [pulp.LpVariable(f'x{k+1}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)])

# Total alloy constraint
problem += pulp.lpSum(x) == data['alloy_quant']

# Metal composition constraints
for m in range(len(data['target'])):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(K)) == data['target'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')