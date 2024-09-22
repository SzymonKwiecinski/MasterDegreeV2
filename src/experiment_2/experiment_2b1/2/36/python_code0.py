import pulp
import json

# Input data
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Problem parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)
M = len(target)

# Create the problem
problem = pulp.LpProblem("Alloy_Mix_Problem", pulp.LpMinimize)

# Decision variables: amount of each alloy to buy
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function: minimize total cost
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)])

# Constraints for the target quantities of metals
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) == target[m]

# Constraint for the total quantity of alloy
problem += pulp.lpSum([amount[k] for k in range(K)]) == alloy_quant

# Solve the problem
problem.solve()

# Gather results
result_amount = [amount[k].varValue for k in range(K)]

# Prepare output
output = {
    "amount": result_amount
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')