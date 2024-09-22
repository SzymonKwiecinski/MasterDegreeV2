import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting the information from the data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(price)  # Number of food items
M = len(demand)  # Number of nutrient types

# Create the linear programming problem
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)  # Quantity of each food item to purchase

# Objective function: Minimize total cost
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints: Nutritional requirements
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Nutrient_Constraint_{m}"

# Solve the problem
problem.solve()

# Output results
result = {"quantity": [quantity[k].varValue for k in range(K)]}
print(json.dumps(result))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')