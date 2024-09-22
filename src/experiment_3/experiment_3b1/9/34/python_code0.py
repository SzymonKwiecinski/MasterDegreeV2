import pulp

# Data from the JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extracting the data
K = len(data['price'])  # Number of food types
M = len(data['demand'])  # Number of nutritional ingredients
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Creating the LP problem
problem = pulp.LpProblem("Nutritional_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("food_quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints for nutritional demands
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demands[m], f"Nutrient_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')