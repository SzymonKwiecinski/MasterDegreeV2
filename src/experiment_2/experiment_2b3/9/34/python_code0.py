import pulp

# Data input
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

prices = data['price']
demands = data['demand']
nutritional_content = data['nutrition']

# Define the problem
problem = pulp.LpProblem("Diet_Optimization", pulp.LpMinimize)

# Number of foods and nutrients
K = len(prices)
M = len(demands)

# Decision variables
quantities = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum([prices[k] * quantities[k] for k in range(K)])

# Constraints: Satisfy nutritional demands
for m in range(M):
    problem += pulp.lpSum([nutritional_content[k][m] * quantities[k] for k in range(K)]) >= demands[m]

# Solve the problem
problem.solve()

# Output the result
result = {"quantity": [pulp.value(quantities[k]) for k in range(K)]}
print(result)

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')