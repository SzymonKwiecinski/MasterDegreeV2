import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],  # Nutrition content of food type 1 for each nutrient
        [1, 3],  # Nutrition content of food type 2 for each nutrient
        [4, 4]   # Nutrition content of food type 3 for each nutrient
    ]
}

# Extract data
prices = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of food types and nutrients
K = len(prices)
M = len(demand)

# Define the LP problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# Nutrient demand constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demand[m], f"Nutrient_{m}_Demand"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')