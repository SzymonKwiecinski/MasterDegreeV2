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

# Problem
problem = pulp.LpProblem("Minimize_Alloy_Production_Cost", pulp.LpMinimize)

# Decision variables
K = len(data['price'])
x = [pulp.LpVariable(f"x_{k}", lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K))

# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == data['alloy_quant']

# Constraint 2: Quantity of each target component in the alloy
M = len(data['target'])
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(K)) >= data['target'][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')