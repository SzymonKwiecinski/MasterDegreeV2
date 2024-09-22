import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting the data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods (K) and nutrients (M)
K = len(price)
M = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables: quantity of each food to purchase
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum([price[k] * quantity[k] for k in range(K)])

# Constraints: Ensure each nutrient demand is met
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(K)]) >= demand[m]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')