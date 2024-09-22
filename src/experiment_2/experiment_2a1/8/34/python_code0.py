import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract parameters from the data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

K = len(prices)  # Number of food items
M = len(demands)  # Number of nutrients

# Create the LP problem
problem = pulp.LpProblem("Minimize_Total_Food_Cost", pulp.LpMinimize)

# Decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(K))

# Constraints: Ensure that nutrient demands are met
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantities[k] for k in range(K)) >= demands[m]

# Solve the problem
problem.solve()

# Output the results
result = {
    "quantity": [quantities[k].varValue for k in range(K)]
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')