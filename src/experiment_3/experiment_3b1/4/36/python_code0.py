import pulp
import json

# Data provided in JSON format
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Model
problem = pulp.LpProblem("AlloyProduction", pulp.LpMinimize)

# Decision Variables
K = len(price)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)]), "Total Cost"

# Constraints

# Total weight of alloys must equal the target weight
problem += pulp.lpSum([amount[k] for k in range(K)]) == alloy_quant, "Total Alloy Weight"

# Constraints for each metal
M = len(target)
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) == target[m], f"Metal {m+1} Requirement"

# Solve the problem
problem.solve()

# Output results
amount_values = [amount[k].varValue for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Amount of each alloy to purchase: {amount_values}')