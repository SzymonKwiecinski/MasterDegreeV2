import pulp

# Data from the provided JSON format
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Parameters
K = len(data['price'])  # Number of different foods
M = len(data['demand'])  # Number of different nutritional ingredients
prices = data['price']
demands = data['demand']
nutrients = data['nutrition']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of food k to purchase

# Objective Function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrients[k][m] * x[k] for k in range(K)) >= demands[m], f"Nutrient_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')