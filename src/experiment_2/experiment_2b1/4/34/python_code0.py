import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data from input
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(price)  # number of food items
M = len(demand)  # number of nutritional demands

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Food_Costs", pulp.LpMinimize)

# Create decision variables for the quantity of each food
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum([price[k] * quantity[k] for k in range(K)])

# Constraints for nutritional demands
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(K)]) >= demand[m]

# Solve the problem
problem.solve()

# Output the quantity of each food purchased
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')