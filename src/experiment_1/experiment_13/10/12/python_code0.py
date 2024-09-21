import pulp
import json

# Data provided in JSON format
data = '{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}'
data = json.loads(data)

# Extract data
alloy_quantity = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

# Indices
K = len(prices)  # number of alloys
M = len(targets)  # number of target components

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraint: total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Alloy_Quantity"

# Constraints: quantity of each target component must be met or exceeded
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= targets[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')