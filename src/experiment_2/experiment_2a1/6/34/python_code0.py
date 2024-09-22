import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data from input
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(prices)
M = len(demands)

# Creating the problem
problem = pulp.LpProblem("Food_Optimization_Problem", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum(prices[k] * quantity[k] for k in range(K)), "Total_Cost"

# Nutritional constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demands[m], f"Nutrient_{m}"

# Solve the problem
problem.solve()

# Output the quantities
quantities = [quantity[k].varValue for k in range(K)]
output = {"quantity": quantities}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')