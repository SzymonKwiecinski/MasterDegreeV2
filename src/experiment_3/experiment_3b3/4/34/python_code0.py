import pulp

# Data from the JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

# Prices, Nutritional values and Demands
prices = data['price']
nutrition = data['nutrition']
demands = data['demand']

# Initialize the optimization problem
problem = pulp.LpProblem("Food_Optimization", pulp.LpMinimize)

# Decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(K)), "Total Cost"

# Nutritional constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantities[k] for k in range(K)) >= demands[m], f"Nutrient_{m}_Demand"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')