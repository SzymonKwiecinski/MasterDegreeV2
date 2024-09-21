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

# Constants
K = len(data['price'])     # Number of alloys
M = len(data['target'])    # Number of components

# Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)])

# Constraints
# Total quantity of alloys produced
problem += pulp.lpSum(x) == data['alloy_quant']

# Quantity of each target component
for m in range(M):
    problem += pulp.lpSum([data['ratio'][k][m] * x[k] for k in range(K)]) >= data['target'][m]

# Solve the problem
problem.solve()

# Print the output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')