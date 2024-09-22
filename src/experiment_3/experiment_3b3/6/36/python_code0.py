import pulp

# Data from the JSON format
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Number of alloys and metals
K = len(data['price'])  # Number of alloys
M = len(data['target'])  # Number of metals

# Create the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
a = [pulp.LpVariable(f'a_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(data['price'][k] * a[k] for k in range(K)), "Total Cost"

# Constraint 1: The total weight of the alloys used must equal the target alloy weight
problem += pulp.lpSum(a[k] for k in range(K)) == data['alloy_quant'], "Total Alloy Quantity"

# Constraint 2: The total amount of each metal m must meet the target
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * a[k] for k in range(K)) == data['target'][m], f"Metal_{m}_Target"

# Solve the problem
problem.solve()

# Output the results
amounts = [pulp.value(a_k) for a_k in a]
print("Amounts purchased for each alloy:", amounts)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')