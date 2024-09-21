import pulp

# Data from the provided JSON format
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

# Number of alloys and targets
K = len(price)  # Number of alloys
M = len(target)  # Number of target components

# Create the linear programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables: quantity of each alloy to produce
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum([price[k] * x[k] for k in range(K)])

# Constraints
# 1. Total quantity of alloys produced must equal alloy_quantity
problem += pulp.lpSum([x[k] for k in range(K)]) == alloy_quantity, "Total_Alloy_Quantity"

# 2. The quantity of each target component must be met or exceeded
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * x[k] for k in range(K)]) >= target[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')