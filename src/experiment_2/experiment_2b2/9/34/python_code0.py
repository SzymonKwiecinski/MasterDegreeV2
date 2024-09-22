import pulp

# Load the data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract data
prices = data["price"]
demands = data["demand"]
nutrition = data["nutrition"]

# Number of foods and nutrients
num_foods = len(prices)
num_nutrients = len(demands)

# Define the problem
problem = pulp.LpProblem("Balanced_Diet_Problem", pulp.LpMinimize)

# Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_foods)]

# Objective function: Minimize the total cost of foods
problem += pulp.lpSum([prices[k] * quantity[k] for k in range(num_foods)])

# Constraints: Meet the nutritional demands
for m in range(num_nutrients):
    problem += pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(num_foods)]) >= demands[m]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(num_foods)]
}

# Print the output
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')