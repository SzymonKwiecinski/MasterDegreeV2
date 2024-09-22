import pulp

# Data
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

# Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)
M = len(target)

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total Cost"

# Constraints
# Total weight constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Weight"

# Target metal weight constraints
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Target_Metal_{m+1}"

# Solve the problem
problem.solve()

# Output the results
result_amounts = [pulp.value(amount[k]) for k in range(K)]
print(f'Optimal amounts of alloys to purchase: {result_amounts}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')