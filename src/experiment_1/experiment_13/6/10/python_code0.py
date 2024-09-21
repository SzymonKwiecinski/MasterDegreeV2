import pulp

# Define the data from the JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extracting parameters from the data
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients

Price = data['price']  # Price of food
Demand = data['demand']  # Demand for nutrients
Nutrition = data['nutrition']  # Nutrition content

# Create the linear programming problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # x_k, number of units purchased from food type k

# Objective Function
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(Nutrition[k][m] * x[k] for k in range(K)) >= Demand[m], f"Nutrient_Requirement_{m}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')