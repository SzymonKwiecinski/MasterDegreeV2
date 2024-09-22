import pulp

# Given Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Set definitions
K = range(len(data['price']))  # food items
M = range(len(data['demand']))  # nutrients

# Create the Linear Programming problem
problem = pulp.LpProblem("Food_Purchase_Optimization", pulp.LpMinimize)

# Decision Variables
quantity = pulp.LpVariable.dicts("quantity", K, lowBound=0)

# Objective Function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in K), "Total_Cost"

# Constraints for each nutrient
for m in M:
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in K) >= data['demand'][m], f"Nutrient_Requirement_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')