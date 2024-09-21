import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extract data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of different types of food (K) and nutrients (M)
K = len(price)
M = len(demand)

# Initialize the problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables: x_k for each food type k
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the total cost
problem += pulp.lpSum(price[k] * x[k] for k in range(K))

# Constraints: Meet or exceed demand for each nutrient
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demand[m]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')