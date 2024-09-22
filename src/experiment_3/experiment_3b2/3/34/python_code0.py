import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Define problem
problem = pulp.LpProblem("Food_Optimization", pulp.LpMinimize)

# Decision variables
K = len(data['price'])  # Number of food items
quantity = [pulp.LpVariable(f'quantity_{k+1}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints
M = len(data['demand'])  # Number of nutrients
for m in range(M):
    problem += (
        pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m],
        f"Nutrient_Requirement_{m+1}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')