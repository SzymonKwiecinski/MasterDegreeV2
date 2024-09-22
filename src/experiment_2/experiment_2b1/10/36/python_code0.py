import pulp
import json

# Input data
data = json.loads("{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}")

# Extracting variables from the data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)
M = len(target)

# Define the problem
problem = pulp.LpProblem("AlloyMixing", pulp.LpMinimize)

# Decision variables for the amount of each alloy
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function: minimize the total cost
problem += pulp.lpSum([amount[k] * price[k] for k in range(K)])

# Constraints for each metal
for m in range(M):
    problem += pulp.lpSum([amount[k] * ratio[k][m] for k in range(K)]) == target[m]

# Constraint for total alloy quantity
problem += pulp.lpSum(amount) == alloy_quant

# Solve the problem
problem.solve()

# Prepare the result
result = {
    "amount": [amount[k].varValue for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')