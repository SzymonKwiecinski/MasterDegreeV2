import pulp
import json

# Data in JSON format
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Model creation
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
K = len(price)  # Number of alloys
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Amounts of each alloy

# Objective Function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints
# 1. Total quantity of alloys must equal alloy_quant
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"

# 2. Constraints for each metal
M = len(target)  # Number of metals
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_{m+1}_Requirement"

# Solve the problem
problem.solve()

# Output the results
amounts = [amount[k].varValue for k in range(K)]
print(f'Amounts of Alloys to Purchase: {amounts}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')