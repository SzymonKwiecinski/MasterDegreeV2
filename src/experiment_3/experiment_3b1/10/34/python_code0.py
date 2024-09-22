import pulp
import json

# Data provided in JSON format
data_json = '{"price": [1, 2, 3], "demand": [10, 20], "nutrition": [[3, 5], [1, 3], [4, 4]]}'
data = json.loads(data_json)

# Extracting data from the JSON
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Sets
K = range(len(price))  # Foods
M = range(len(demand))  # Nutrients

# Creating the linear programming problem
problem = pulp.LpProblem("Nutritional_Diet_Problem", pulp.LpMinimize)

# Variables
quantity = pulp.LpVariable.dicts("quantity", K, lowBound=0)

# Objective Function
problem += pulp.lpSum(price[k] * quantity[k] for k in K), "Total Cost"

# Constraints for nutrients
for m in M:
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in K) >= demand[m], f"Nutrient_Requirement_{m}"

# Solving the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')