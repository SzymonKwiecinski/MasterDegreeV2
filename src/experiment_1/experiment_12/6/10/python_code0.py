import pulp

# Data from JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],
        [1, 3],
        [4, 4]
    ]
}

# Parameters
K = len(data['price'])  # Number of food types
M = len(data['demand'])  # Number of nutrients

# Create LP problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K))

# Constraints: Meet nutrient demands
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')