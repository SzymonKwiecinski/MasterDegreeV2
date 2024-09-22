import pulp
import json

# Data input
data = json.loads('{"price": [1, 2, 3], "demand": [10, 20], "nutrition": [[3, 5], [1, 3], [4, 4]]}')

# Extract data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of food items and nutrients
K = len(prices)
M = len(demands)

# Create the problem
problem = pulp.LpProblem("Food_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("food", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demands[m], f"Nutrient_{m+1}_Demand"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')