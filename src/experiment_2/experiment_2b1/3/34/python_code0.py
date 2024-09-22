import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting parameters from input data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']
K = len(prices)  # Number of foods
M = len(demands)  # Number of nutrients

# Creating the problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demands[m], f"Nutrient_{m+1}_Demand"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
print(json.dumps(output))