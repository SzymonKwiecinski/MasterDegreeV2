import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data from the input
prices = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(prices)
M = len(demand)

# Creating the linear programming problem
problem = pulp.LpProblem("MinimizeFoodCost", pulp.LpMinimize)

# Decision variables: quantity of each food to purchase
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective function: minimize total cost
problem += pulp.lpSum(prices[k] * quantity[k] for k in range(K)), "TotalCost"

# Constraints: ensuring the nutritional needs are met
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"NutrientDemand_{m}"

# Solve the problem
problem.solve()

# Collecting the results
result_quantity = [quantity[k].varValue for k in range(K)]

# Output the results
output = {"quantity": result_quantity}
print(json.dumps(output))

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')