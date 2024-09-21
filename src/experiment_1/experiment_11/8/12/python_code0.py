import pulp

# Data from the provided JSON format
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Problem definition
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
K = len(data['price'])  # Number of alloys
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)]), "Total_Cost"

# Constraints
# 1. Total quantity of alloys produced
problem += pulp.lpSum([x[k] for k in range(K)]) == data['alloy_quant'], "Total_Alloy_Quantity"

# 2. Quantity of each target component in the alloy must be met or exceeded
M = len(data['target'])  # Number of target components
for m in range(M):
    problem += pulp.lpSum([data['ratio'][k][m] * x[k] for k in range(K)]) >= data['target'][m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Print the optimal objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')