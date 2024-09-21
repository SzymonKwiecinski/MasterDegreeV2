import pulp

# Data based on the provided JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extract data
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients to consider
Price = data['price']
Demand = data['demand']
Nutrition = data['nutrition']

# Initialize problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the total cost of the foods purchased
problem += pulp.lpSum([Price[k] * x[k] for k in range(K)]), "Total_Cost"

# Constraints: 
# The total amount of each nutrient from all food types must meet or exceed the specific demand for that nutrient
for m in range(M):
    problem += pulp.lpSum([Nutrition[k][m] * x[k] for k in range(K)]) >= Demand[m], f"Nutrition_Requirement_{m}"

# Solve the problem
problem.solve()

# Print the result
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")