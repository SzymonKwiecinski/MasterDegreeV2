import pulp

# Problem data
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

# Number of metals and alloys
M = len(target)
K = len(prices)

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Variables: amount of each alloy to buy
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost
problem += pulp.lpSum(prices[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints: Ensure that the alloy composition meets the target
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_{m}_Target"

# Constraint: Total weight of alloys should be equal to alloy_quant
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Weight"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "amount": [pulp.value(amount_k) for amount_k in amount]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')