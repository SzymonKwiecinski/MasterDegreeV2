import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']
K = len(price)  # Number of food items
M = len(demand)  # Number of nutrients

# Creating the linear programming problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints: Nutritional requirements
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Demand_Constraint_{m}"

# Solve the problem
problem.solve()

# Output results
quantities = [quantity[k].varValue for k in range(K)]
output = {"quantity": quantities}
print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')