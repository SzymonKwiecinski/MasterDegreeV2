import pulp

# Data from the provided JSON format
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Parameters
AlloyQuantity = data['alloy_quant']
Target = data['target']
Ratio = data['ratio']
Price = data['price']

# Number of alloys and components
K = len(Price)  # number of alloys
M = len(Target)  # number of target components

# Create the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # x[k] >= 0

# Objective Function
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# 1. Total quantity of alloys produced is exactly AlloyQuantity
problem += pulp.lpSum(x[k] for k in range(K)) == AlloyQuantity, "Total_Alloy_Quantity"

# 2. Each target component requirement must be met or exceeded
for m in range(M):
    problem += pulp.lpSum(Ratio[k][m] * x[k] for k in range(K)) >= Target[m], f"Target_Requirement_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')