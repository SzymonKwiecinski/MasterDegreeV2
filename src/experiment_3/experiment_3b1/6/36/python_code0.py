import pulp
import json

# Data
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

A = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Define the problem
problem = pulp.LpProblem("Alloy_Production_Optimization", pulp.LpMinimize)

# Define variables
K = len(price)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Total weight constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == A, "Total_Weight"

# Metal composition constraints
for m in range(len(target)):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_Composition_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')