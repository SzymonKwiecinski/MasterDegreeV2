import pulp

# Data from the JSON
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

# Extracting data
AlloyQuantity = data['alloy_quant']
Target = data['target']
Ratio = data['ratio']
Price = data['price']
K = len(Price)
M = len(Target)

# Problem Definition
problem = pulp.LpProblem("Alloy Production", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "Total Cost"

# Constraints
# 1. Total quantity of alloys
problem += pulp.lpSum(x[k] for k in range(K)) == AlloyQuantity, "Total_Alloy_Quantity"

# 2. Quantity of each target component
for m in range(M):
    problem += pulp.lpSum(Ratio[k][m] * x[k] for k in range(K)) >= Target[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')