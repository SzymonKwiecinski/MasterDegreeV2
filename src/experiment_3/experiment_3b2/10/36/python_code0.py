import pulp

# Data from the JSON format
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Parameters
alloy_quant = data['alloy_quant']
target_m = data['target']
ratio = data['ratio']
price = data['price']
K = len(price)  # Number of alloys

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
amount_k = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * amount_k[k] for k in range(K)), "Total_Cost"

# Constraints
problem += pulp.lpSum(amount_k[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"

for m in range(len(target_m)):
    problem += pulp.lpSum(ratio[k][m] * amount_k[k] for k in range(K)) == target_m[m], f"Target_Metal_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')