import pulp
import json

# Data provided in JSON format
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Extracting data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)
M = len(target)

# Create the LP problem
problem = pulp.LpProblem("AlloyProduction", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total Cost"

# Constraints
# Constraint 1: Total weight of alloys must equal alloy_quant
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total Weight Constraint"

# Constraints for each metal
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"Metal_{m+1}_Constraint"

# Solve the problem
problem.solve()

# Output the results
amount = [x[k].varValue for k in range(K)]
print(f"Amount of each alloy to purchase: {amount}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')