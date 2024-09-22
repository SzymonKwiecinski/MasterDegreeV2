import pulp

# Data from JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],
        [1, 3],
        [4, 4]
    ]
}

# Number of foods (K) and nutrients (M)
K = len(data['price'])
M = len(data['demand'])

# Define the LP problem
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

# Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize total price
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K))

# Constraints: Meet the demand for each nutrient
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m]

# Solve the problem
problem.solve()

# Output the results
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')