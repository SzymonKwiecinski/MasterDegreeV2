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

# Extract data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # Number of available alloys
M = len(target)  # Number of metals in the target alloy

# Define the problem
problem = pulp.LpProblem("Minimum_Cost_Alloy_Production", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the total cost
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)])

# Constraints
# Each metal must meet its target requirement
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) >= target[m]

# The total amount of alloys should sum up to the desired quantity
problem += pulp.lpSum([amount[k] for k in range(K)]) == alloy_quant

# Solve the problem
problem.solve()

# Output the results
result = {
    "amount": [pulp.value(amount[k]) for k in range(K)]
}
print(result)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')