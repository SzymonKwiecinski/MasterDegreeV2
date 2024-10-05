import pulp

# Read the JSON data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(price)
M = len(demand)

# Define the linear programming problem
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

# Variables: quantity of each food
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the total cost
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K))

# Constraints: Satisfy the nutritional demand for each nutrient
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m]

# Solve the problem
problem.solve()

# Collect results
result = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')