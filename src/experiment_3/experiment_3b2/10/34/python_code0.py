import pulp
import json

# Data
data = json.loads('{"price": [1, 2, 3], "demand": [10, 20], "nutrition": [[3, 5], [1, 3], [4, 4]]}')
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Problem setup
K = len(price)  # Number of food items
M = len(demand)  # Number of nutritional demands

# Create the linear programming problem
problem = pulp.LpProblem("Food_Purchase_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demand[m], f"Nutritional_Demand_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')