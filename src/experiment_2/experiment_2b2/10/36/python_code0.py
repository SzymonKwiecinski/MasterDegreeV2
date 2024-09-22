import pulp

# Data from the JSON input
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [
        [0.1, 0.9], 
        [0.25, 0.75], 
        [0.5, 0.5], 
        [0.75, 0.25], 
        [0.95, 0.05]
    ],
    'price': [5, 4, 3, 2, 1.5]
}

# Extracting the values
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys
K = len(price)
# Number of metals
M = len(target)

# Initialize the problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision variables: Amount of each metal to purchase
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the cost
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)])

# Constraints: Ensure the mix matches the target alloy composition
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) == target[m]

# Solve the problem
problem.solve()

# Collecting the results
result = {
    "amount": [amount[k].varValue for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')