import pulp

# Given data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting the data
prices = data["price"]
demands = data["demand"]
nutrition_matrix = data["nutrition"]

# Number of foods and nutrients
K = len(prices)
M = len(demands)

# Initialize the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables: quantity of each food to purchase
quantity_vars = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum([prices[k] * quantity_vars[k] for k in range(K)])

# Nutritional constraints
for m in range(M):
    problem += pulp.lpSum([nutrition_matrix[k][m] * quantity_vars[k] for k in range(K)]) >= demands[m]

# Solve the problem
problem.solve()

# Collect the results
quantities = [pulp.value(quantity_vars[k]) for k in range(K)]

# Print the output
output = {"quantity": quantities}
print(output)

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')