import pulp
import json

# Data input
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Problem parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # number of alloys
M = len(target)  # number of metals

# Creating the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total Cost"

# Constraints
# Total weight must equal the desired alloy weight
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total Alloys Weight"

# Constraints for each metal
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_{m+1}_Requirement"

# Solve the problem
problem.solve()

# Output the results
amount_values = {k: amount[k].varValue for k in range(K)}
print(f'Amount of each alloy to purchase: {amount_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')