import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

K = len(data['price'])  # Number of different foods
M = len(data['demand'])  # Number of different nutrients

# Create a linear programming problem
problem = pulp.LpProblem("Food_Purchase_Optimization", pulp.LpMinimize)

# Create decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints for nutritional requirements
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m], f"Nutrient_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')