import pulp

# Data from JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extracting data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of food items
num_foods = len(prices)

# Number of nutritional constraints
num_nutrients = len(demands)

# Define the problem
problem = pulp.LpProblem("Diet_Optimization_Problem", pulp.LpMinimize)

# Define decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_foods)]

# Objective function: Minimize total cost
problem += pulp.lpSum([prices[k] * quantities[k] for k in range(num_foods)]), "Total_Cost"

# Constraints: Nutritional requirements
for m in range(num_nutrients):
    problem += pulp.lpSum([nutrition[k][m] * quantities[k] for k in range(num_foods)]) >= demands[m], f'Nutrient_{m}'

# Solve the problem
problem.solve()

# Output the result
for k in range(num_foods):
    print(f'quantity_{k}: {pulp.value(quantities[k])}')

print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')