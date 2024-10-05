import pulp

# Data from the problem description
data = {
    "alloy_quant": 1000, 
    "target": [300, 700], 
    "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
    "price": [5, 4, 3, 2, 1.5]
}

# Problem Data
alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

# Problem definition
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables: amount of each alloy
amount = [pulp.LpVariable(f"amount_{k}", lowBound=0) for k in range(len(prices))]

# Objective Function: Minimize cost of alloys
problem += pulp.lpSum([prices[k] * amount[k] for k in range(len(prices))]), "Total Cost"

# Constraints: 
# 1. Meet the target metal composition in the final alloy
for m in range(len(target)):
    problem += pulp.lpSum([ratios[k][m] * amount[k] for k in range(len(prices))]) == target[m], f"Metal_{m}_Target"

# 2. Total amount of alloy produced should be equal to alloy_quant
problem += pulp.lpSum(amount) == alloy_quant, "Total_Alloy_Amount"

# Solve the problem
problem.solve()

# Output the amounts needed for each alloy to minimize cost
result = {
    "amount": [pulp.value(amount_k) for amount_k in amount]
}
print(result)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')