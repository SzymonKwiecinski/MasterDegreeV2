import json
import pulp

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting the data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Define the problem
problem = pulp.LpProblem("Minimize_Food_Costs", pulp.LpMinimize)

# Define the variables
K = len(price)  # Number of food types
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([price[k] * quantity[k] for k in range(K)])

# Constraints
M = len(demand)  # Number of nutrients
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(K)]) >= demand[m]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

# Print the results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')