import pulp

# Given data
data = {
    'price': [1, 2, 3],  # Prices of food types
    'demand': [10, 20],  # Nutrient demands
    'nutrition': [[3, 5], [1, 3], [4, 4]]  # Nutritional content
}

# Parameters
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients

# Create the linear programming problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Units purchased from each food type

# Objective Function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)]), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum([data['nutrition'][k][m] * x[k] for k in range(K)]) >= data['demand'][m], f"Nutrient_Requirement_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')