import pulp

# Data from the input format
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract parameters from data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

K = len(price)  # Number of different foods
M = len(demand)  # Number of nutritional ingredients

# Define the problem
problem = pulp.LpProblem("BalancedDiet", pulp.LpMinimize)

# Decision variables: quantity of each food to purchase
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the total price of the foods
problem += pulp.lpSum([price[k] * quantity[k] for k in range(K)])

# Constraints: Each nutritional demand must be met
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(K)]) >= demand[m]

# Solve the problem
problem.solve()

# Extract the result
result = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

# Output the result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')