import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extract data
K = len(data['price'])  # Number of food types
M = len(data['demand'])  # Number of nutrients
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Initialize the problem
problem = pulp.LpProblem("Minimize_Cost_Balanced_Diet", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Nutritional requirements constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demand[m], f"Nutritional_Requirement_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')