import pulp

# Load data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(price)
M = len(demand)

# Create a LP Minimization problem
problem = pulp.LpProblem("Minimize Food Cost", pulp.LpMinimize)

# Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K))

# Constraints: Meet the nutritional demands
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m]

# Solve the problem
problem.solve()

# Output results
results = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')