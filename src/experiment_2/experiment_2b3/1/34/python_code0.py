import pulp

# Parse the input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract data components
prices = data['price']
demands = data['demand']
nutritions = data['nutrition']

# Number of foods and nutrients
num_foods = len(prices)
num_nutrients = len(demands)

# Create the LP problem instance
problem = pulp.LpProblem("Balanced_Diet_Problem", pulp.LpMinimize)

# Define decision variables for the quantity of each food
quantity_vars = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_foods)]

# Objective function: minimize the total price
total_cost = pulp.lpSum([prices[k] * quantity_vars[k] for k in range(num_foods)])
problem += total_cost

# Constraints: meet the demand for each nutrient
for m in range(num_nutrients):
    nutrient_constraint = pulp.lpSum([nutritions[k][m] * quantity_vars[k] for k in range(num_foods)]) >= demands[m]
    problem += nutrient_constraint

# Solve the problem
problem.solve()

# Collect results
result_quantity = [pulp.value(quantity_vars[k]) for k in range(num_foods)]

# Prepare output
output = {"quantity": result_quantity}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')