import pulp

# Data from the problem
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract data
prices = data['price']
demands = data['demand']
nutritions = data['nutrition']

# Number of foods and nutrients
num_foods = len(prices)
num_nutrients = len(demands)

# Create a problem instance
problem = pulp.LpProblem("Balanced_Diet", pulp.LpMinimize)

# Decision variables: quantity of each food to purchase
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_foods)]

# Objective function: Minimize the total cost
problem += pulp.lpSum([prices[k] * quantities[k] for k in range(num_foods)])

# Constraints: Nutritional demands must be satisfied
for m in range(num_nutrients):
    problem += pulp.lpSum([nutritions[k][m] * quantities[k] for k in range(num_foods)]) >= demands[m]

# Solve the problem
problem.solve()

# Output quantities
quantity_result = [pulp.value(quantities[k]) for k in range(num_foods)]
output = {'quantity': quantity_result}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')