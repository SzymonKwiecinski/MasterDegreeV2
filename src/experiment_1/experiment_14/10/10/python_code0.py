import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],  # Nutrients in Food 1
        [1, 3],  # Nutrients in Food 2
        [4, 4]   # Nutrients in Food 3
    ]
}

# Extract data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(prices)
M = len(demands)

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Food_Selection", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K))

# Constraints for nutrient demands
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demands[m], f"Demand_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')