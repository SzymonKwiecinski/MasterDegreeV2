import pulp

# Data from the provided JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
K = len(data['price'])  # Number of food types
M = len(data['demand'])  # Number of nutritional ingredients
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Create the LP problem
problem = pulp.LpProblem("FoodPurchaseOptimization", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([price[k] * quantity[k] for k in range(K)]), "Total Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(K)]) >= demand[m], f"Nutrient_{m + 1}_Requirement"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')