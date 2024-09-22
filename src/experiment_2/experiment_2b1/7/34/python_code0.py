import pulp
import json

# Provided input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data from the input
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Define the problem
problem = pulp.LpProblem("Minimize_Food_Costs", pulp.LpMinimize)

# Number of foods and nutrients
K = len(price)
M = len(demand)

# Decision variables: quantity of each food to purchase
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize total price
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K))

# Constraints: Ensure that the nutritional demands are met
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m]

# Solve the problem
problem.solve()

# Preparing the output
output_quantity = [quantity[k].varValue for k in range(K)]

# Print the output
print(json.dumps({"quantity": output_quantity}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')