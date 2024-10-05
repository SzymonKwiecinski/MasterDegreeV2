import pulp

# Input data from JSON
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting the data
prices = data["price"]
demands = data["demand"]
nutrition = data["nutrition"]

# Number of food items and nutrients
K = len(prices)
M = len(demands)

# Define the LP problem
problem = pulp.LpProblem("Nutritional_Diet", pulp.LpMinimize)

# Define decision variables: quantity of each food to purchase
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost of foods
problem += pulp.lpSum([prices[k] * quantities[k] for k in range(K)])

# Nutritional constraints: Ensure each nutrient demand is met
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * quantities[k] for k in range(K)]) >= demands[m]

# Solve the problem
problem.solve()

# Prepare output
output = {"quantity": [pulp.value(quantities[k]) for k in range(K)]}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')