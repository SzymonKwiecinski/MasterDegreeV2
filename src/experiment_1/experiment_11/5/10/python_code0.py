import pulp

# Data from JSON
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data
K = len(data['price'])  # Number of food types
M = len(data['demand'])  # Number of nutrients
Price = data['price']
Demand = data['demand']
Nutrition = data['nutrition']

# Create the linear programming problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # x_k >= 0 for all k

# Objective function
problem += pulp.lpSum([Price[k] * x[k] for k in range(K)]), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum([Nutrition[k][m] * x[k] for k in range(K)]) >= Demand[m], f"Nutrient_Conservation_{m+1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')