import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data from JSON format
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of food items and nutrients
K = len(price)
M = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables: quantity of each food to purchase
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints: Ensure demand for each nutrient is met
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Nutrient_Demand_{m}"

# Solve the problem
problem.solve()

# Output results
result_quantities = [quantity[k].varValue for k in range(K)]
output = {"quantity": result_quantities}
print(output)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')