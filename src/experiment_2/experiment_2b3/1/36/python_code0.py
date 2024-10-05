import pulp

# Data
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

# Variables
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)
M = len(target)

# Problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective Function
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)])

# Constraints
for m in range(M):
    problem += (pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) == target[m])

# Solve
problem.solve()

# Results
amount_result = [amount[k].varValue for k in range(K)]
result = {"amount": amount_result}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')