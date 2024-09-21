import pulp
import json

# Input data
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Parameters
alloy_quantity = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  # Number of alloys
M = len(targets)  # Number of target components

# Create the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# Total quantity of alloys produced equals AlloyQuantity
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Quantity_Constraint"

# Target components constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= targets[m], f"Target_Component_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')