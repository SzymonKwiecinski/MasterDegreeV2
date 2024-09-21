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

# Set parameters
K = len(data['price'])  # Number of alloys
M = len(data['target'])  # Number of target components

# Create a linear programming problem
problem = pulp.LpProblem("Alloy_Production_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# 1. Total quantity of alloys
problem += pulp.lpSum(x[k] for k in range(K)) == data['alloy_quant'], "Total_Quantity"

# 2. Component constraints
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(K)) >= data['target'][m], f"Component_{m}_Requirement"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')