import pulp
import json

# Data
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision Variables
K = len(price)  # Number of alloys
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints
# Alloy Quantity Constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Alloy_Quantity_Constraint"

# Metal Quantity Constraints
M = len(target)  # Number of metals
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_Quantity_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Output results
amounts = [amount[k].varValue for k in range(K)]
print(f'Amounts: {amounts}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')