import pulp
import json

# Data
data = json.loads('{"price": [1, 2, 3], "demand": [10, 20], "nutrition": [[3, 5], [1, 3], [4, 4]]}')
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Parameters
K = len(price)  # Number of different types of food
M = len(demand)  # Number of nutrients

# Create the problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demand[m], f"Nutrient_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')