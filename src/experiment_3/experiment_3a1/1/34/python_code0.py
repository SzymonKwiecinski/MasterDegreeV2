import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
K = len(data['price'])  # Number of foods
M = len(data['demand'])  # Number of nutrients

# Create a linear programming problem
problem = pulp.LpProblem("Balanced_Diet", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Food", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)]), "Total_Cost"

# Constraints for nutritional demands
for m in range(M):
    problem += pulp.lpSum([data['nutrition'][k][m] * x[k] for k in range(K)]) >= data['demand'][m], f"Nutrient_{m+1}_Demand"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')