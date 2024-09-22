import pulp

# Define the data from the JSON format
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

# Define the problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

K = len(data['price'])
M = len(data['target'])

# Define the decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Define the objective function
problem += pulp.lpSum(data['price'][k] * amount[k] for k in range(K)), "Total_Cost"

# Metal content constraints
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * amount[k] for k in range(K)) == data['target'][m], f"Metal_{m}_Content"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "amount": [pulp.value(amount[k]) for k in range(K)]
}

print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')