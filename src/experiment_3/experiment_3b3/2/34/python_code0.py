import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Indices for foods and nutrients
K = len(data['price'])  # Number of foods
M = len(data['demand'])  # Number of nutrients

# Create a linear programming problem
problem = pulp.LpProblem("Dietary_Optimization", pulp.LpMinimize)

# Decision variables: quantities of food k purchased
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize total cost of food
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints: Nutritional requirements
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Nutrient_{m+1}_Requirement"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')