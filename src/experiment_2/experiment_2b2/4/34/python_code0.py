import pulp

# Given data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
num_foods = len(prices)
num_nutrients = len(demands)

# Define the Linear Programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Define decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_foods)]

# Objective function: Minimize total cost of foods
problem += pulp.lpSum([prices[k] * quantities[k] for k in range(num_foods)])

# Constraints: Each nutrient requirement must be met
for m in range(num_nutrients):
    problem += pulp.lpSum([nutrition[k][m] * quantities[k] for k in range(num_foods)]) >= demands[m]

# Solve the problem
problem.solve()

# Print the quantity of each food to purchase
output = {"quantity": [pulp.value(quantities[k]) for k in range(num_foods)]}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')