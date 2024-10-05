import pulp

# Parse the data from the JSON format
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # Number of available alloys
M = len(target)  # Number of metals

# Define the LP problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Define decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective Function: Minimize cost
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)])

# Constraints: Achieve the target metal composition
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) == target[m]

# Total alloy quantity constraint
problem += pulp.lpSum(amount) == alloy_quant

# Solve the problem
problem.solve()

# Extracting results
amount_solution = [pulp.value(amount[k]) for k in range(K)]

# Format the result as specified
result = {
    "amount": amount_solution
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')