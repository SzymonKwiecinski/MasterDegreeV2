import pulp

# Data from JSON
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Parameters
prices = data['price']
demands = data['demand']
nutritional_values = data['nutrition']

# Number of food items and nutrients
K = len(prices)
M = len(demands)

# Problem
problem = pulp.LpProblem("Food_Purchase_Problem", pulp.LpMinimize)

# Decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(K)), "Total_Cost"

# Nutritional constraints
for m in range(M):
    problem += (pulp.lpSum(nutritional_values[k][m] * quantities[k] for k in range(K)) >= demands[m], f"Nutrient_{m}")

# Solve problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')