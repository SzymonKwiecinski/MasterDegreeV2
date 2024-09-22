import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Problem
problem = pulp.LpProblem("Balanced_Diet_Problem", pulp.LpMinimize)

# Variables
K = len(data['price'])
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K))

# Constraints
M = len(data['demand'])
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m]

# Solve
problem.solve()

# Output
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')