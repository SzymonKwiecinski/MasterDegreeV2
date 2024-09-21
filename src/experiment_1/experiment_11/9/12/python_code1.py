import pulp

# Data from JSON format
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Parameters
alloy_quantity = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
K = len(price)  # Number of alloys
M = len(target)  # Number of components

# Create the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Quantity"

# Constraint 2: Each target component in the alloy must be met or exceeded
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) >= target[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')