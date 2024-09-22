import pulp
import json

# Given data
data = json.loads('{"price": [1, 2, 3], "demand": [10, 20], "nutrition": [[3, 5], [1, 3], [4, 4]]}')

# Parameters
K = len(data['price'])  # Number of food items
M = len(data['demand'])  # Number of nutrient requirements
prices = data['price']
demands = data['demand']
nutri = data['nutrition']

# Create the problem
problem = pulp.LpProblem("Minimize_Cost_of_Food", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # x_k >= 0

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutri[k][m] * x[k] for k in range(K)) >= demands[m], f"Nutrient_Requirement_{m}"

# Solve the problem
problem.solve()

# Output the quantities and objective value
for k in range(K):
    print(f"Quantity of food {k+1} to purchase: {x[k].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')