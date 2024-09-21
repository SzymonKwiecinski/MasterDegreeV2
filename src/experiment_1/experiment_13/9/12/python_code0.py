import pulp
import json

# Data from JSON format
data = {
    'alloy_quant': 1000, 
    'target': [300, 700], 
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
    'price': [5, 4, 3, 2, 1.5]
}

# Extracting parameters
alloy_quantity = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # number of alloys
M = len(target)  # number of components

# Create the optimization problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Alloy", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# Total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Alloy_Quantity"

# Quantity of each target component met or exceeded
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) >= target[m], f"Target_Requirement_{m + 1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')