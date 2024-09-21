import pulp

# Data from the JSON format
data = {
    'price': [1, 2, 3], 
    'demand': [10, 20], 
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients

# Create the problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("food", range(K), lowBound=0)  # x_k >= 0

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Nutrient_{m+1}_Demand"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')