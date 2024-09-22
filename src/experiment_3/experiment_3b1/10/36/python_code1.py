import pulp
import json

# Data (parsed from the provided JSON format)
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Extracting data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)  # number of alloys
M = len(target)  # number of metals

# Create a linear programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints
# Total amount produced must equal alloy_quant
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"

# Constraints for each metal
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_{m+1}_Target"

# Solve the problem
problem.solve()

# Output the amounts of each alloy
amounts = [amount[k].varValue for k in range(K)]
print(f'Output: {{ "amount": {amounts} }}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')