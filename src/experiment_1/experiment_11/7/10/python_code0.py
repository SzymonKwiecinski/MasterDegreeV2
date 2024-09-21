import pulp

# Data from the JSON input
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients

# Create the problem instance
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total Cost"

# Constraints
for m in range(M):
    problem += (pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m]), f"Nutrient_Requirement_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')