import pulp

# Input data
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

# Extract data from the input
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # Number of different alloys

# Define the Linear Programming problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Define the decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost of the alloys
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints: Achieve the desired target quantities for each metal
for m in range(len(target)):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_{m}_Constraint"

# Solve the problem
problem.solve()

# Collect results
result = {
    "amount": [pulp.value(amount[k]) for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')