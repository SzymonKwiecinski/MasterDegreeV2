import pulp

# Data from the problem
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients to consider
Price = data['price']
Demand = data['demand']
Nutrition = data['nutrition']

# Create the problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(Price[k] * x[k] for k in range(K))

# Constraints
for m in range(M):
    problem += pulp.lpSum(Nutrition[k][m] * x[k] for k in range(K)) >= Demand[m]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')