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

# Constants
alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

# Number of alloys and components
K = len(prices)
M = len(target)

# Initialize the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost of the alloys
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraint 1: Total quantity of alloys produced is exactly AlloyQuantity
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Quantity"

# Constraint 2: Quantity of each target component in the alloy
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= target[m], f"Component_Target_{m}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')