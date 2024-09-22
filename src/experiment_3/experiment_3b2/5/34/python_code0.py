import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Define the problem
problem = pulp.LpProblem("Nutritional_Diet_Problem", pulp.LpMinimize)

# Decision variables
K = len(data['price'])  # Number of food items
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of each food item

# Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
M = len(data['demand'])  # Number of nutritional demands
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Demand_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')