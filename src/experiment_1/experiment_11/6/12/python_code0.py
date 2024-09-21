import pulp
import json

# Data initialization from JSON
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Problem parameters
alloy_quantity = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # Number of alloys
M = len(target)  # Number of target components

# Define the linear programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Alloy", range(K), lowBound=0)  # Non-negative decision variables for each alloy

# Objective Function: Minimize total cost of the alloys
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# 1. Total quantity of alloys produced is exactly AlloyQuantity
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Alloys"

# 2. Quantity of each target component must be met or exceeded
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) >= target[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')