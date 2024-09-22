import pulp

# Data from the problem description
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data elements
prices = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Indices
num_foods = len(prices)
num_nutrients = len(demand)

# Problem
problem = pulp.LpProblem("DietProblem", pulp.LpMinimize)

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_foods)]

# Objective
problem += pulp.lpSum([prices[k] * quantity[k] for k in range(num_foods)])

# Constraints
for m in range(num_nutrients):
    problem += pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(num_foods)]) >= demand[m]

# Solve
problem.solve()

# Output
quantity_values = [pulp.value(quantity[k]) for k in range(num_foods)]
output = {'quantity': quantity_values}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')