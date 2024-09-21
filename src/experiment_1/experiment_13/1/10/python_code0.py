import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of food types (K) and nutrients (M)
K = len(data['price'])
M = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("FoodUnits", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints for each nutrient
for m in range(M):
    problem += (pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m],
                 f"Nutrient_Constraint_{m}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')