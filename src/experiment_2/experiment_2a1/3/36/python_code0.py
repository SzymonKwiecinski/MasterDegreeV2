import pulp
import json

# Input data from JSON format
data = json.loads("{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}")

# Problem parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
K = len(price)  # Number of available alloys
M = len(target)  # Number of metals

# Define the problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Define decision variables
amounts = pulp.LpVariable.dicts("Alloy_Amount", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(price[k] * amounts[k] for k in range(K)), "Total_Cost"

# Constraints
problem += pulp.lpSum(amounts[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amounts[k] for k in range(K)) == target[m], f"Metal_{m+1}_Target"

# Solve the problem
problem.solve()

# Output results
amount = [amounts[k].varValue for k in range(K)]
output = {"amount": amount}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')