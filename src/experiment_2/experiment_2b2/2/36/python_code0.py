import pulp

# Data from JSON
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

# Problem setup
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(len(data['price']))]

# Objective function: Minimize cost
problem += pulp.lpSum([data['price'][k] * amount[k] for k in range(len(data['price']))])

# Constraints
# Total weight constraint
problem += pulp.lpSum(amount) == data['alloy_quant']

# Metal content constraints
for m in range(len(data['target'])):
    problem += pulp.lpSum([data['ratio'][k][m] * amount[k] for k in range(len(data['price']))]) == data['target'][m]

# Solve the problem
problem.solve()

# Collect results
result = {'amount': [pulp.value(amount[k]) for k in range(len(data['price']))]}

# Output the result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')