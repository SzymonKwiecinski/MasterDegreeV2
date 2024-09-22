import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of foods and nutrients
K = len(data['price'])  # Number of food items
M = len(data['demand'])  # Number of nutrients

# Create the Linear Programming problem
problem = pulp.LpProblem("Nutrition_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Food", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K))

# Constraints for nutritional requirements
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')