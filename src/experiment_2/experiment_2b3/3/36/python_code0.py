import pulp

# Data input
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

M = len(target)  # Number of metals
K = len(price)   # Number of available alloys

# Problem definition
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision variables: amounts of each alloy k to buy
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost of alloys
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints: Satisfy the target metal composition required
for m in range(M):
    problem += (pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m]), f'Metal_Constraint_{m}'

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "amount": [pulp.value(amount[k]) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')