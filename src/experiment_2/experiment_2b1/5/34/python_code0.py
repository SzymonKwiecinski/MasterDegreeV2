import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(price)
M = len(demand)

# Problem definition
problem = pulp.LpProblem("MinimizeFoodCost", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K))

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m]

# Solve the problem
problem.solve()

# Extract results
quantities = [quantity[k].varValue for k in range(K)]

# Output results
output = {'quantity': quantities}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')