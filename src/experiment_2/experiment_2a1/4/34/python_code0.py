import pulp
import json

data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract data from JSON input
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of food types and nutrients
K = len(price)
M = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Create decision variables for the quantities of each food type
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints for each nutrient
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Nutrient_Constraint_{m}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')