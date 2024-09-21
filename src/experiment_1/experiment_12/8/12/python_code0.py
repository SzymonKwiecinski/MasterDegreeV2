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
K = len(prices)  # Number of alloys
M = len(targets)  # Number of components

# Problem
problem = pulp.LpProblem("Alloy_Production_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total Cost"

# Constraints
# Total quantity constraint
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total Alloy Quantity"

# Target component constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= targets[m], f"Target_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')