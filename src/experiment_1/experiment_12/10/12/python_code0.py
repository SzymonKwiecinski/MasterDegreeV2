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

# Number of alloys (K) and number of components (M)
K = len(data['price'])
M = len(data['target'])

# Initialize the problem
problem = pulp.LpProblem("Alloy_Production_Minimization", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0) for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K))

# Constraints
# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum(x) == data['alloy_quant']

# Constraint 2: Quantity of each target component met or exceeded
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(K)) >= data['target'][m]

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')