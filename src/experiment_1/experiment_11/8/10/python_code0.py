import pulp

# Data
data = {
    'price': [1, 2, 3],  # Prices for food types 1, 2, 3
    'demand': [10, 20],  # Nutrient demands for nutrient 1 and 2
    'nutrition': [[3, 5], [1, 3], [4, 4]]  # Nutrition values
}

# Parameters
K = len(data['price'])  # Number of food types
M = len(data['demand'])  # Number of nutrients

# Decision Variables
x = pulp.LpVariable.dicts('x', range(K), lowBound=0)

# Create the problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Nutrient_Demand_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')