import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting parameters from the data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of foods (K) and nutrients (M)
K = len(prices)
M = len(demands)

# Create the problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective function: minimize total cost
problem += pulp.lpSum(prices[k] * quantity[k] for k in range(K))

# Constraints: meet nutritional demands
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demands[m]

# Solve the problem
problem.solve()

# Output results
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')