import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract the data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods (K) and nutrients (M)
K = len(price)
M = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize total price
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints: Ensure nutritional demand is met
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Nutrient_Constraint_{m}"

# Solve the problem
problem.solve()

# Output the quantities
result = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

# Print the result and the objective value
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')