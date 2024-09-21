import pulp

# Data extracted from the provided JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Define the parameters
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients

# Create the LP problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints for each nutrient
for m in range(M):
    problem += (pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m]), f"Nutrient_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')