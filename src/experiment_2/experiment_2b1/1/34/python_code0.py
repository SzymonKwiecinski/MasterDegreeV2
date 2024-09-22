import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Define parameters
K = len(data['price'])  # number of foods
M = len(data['demand'])  # number of nutrients
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Define the problem
problem = pulp.LpProblem("MinimizeFoodCost", pulp.LpMinimize)

# Define decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "TotalCost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"NutrientDemand_{m}"

# Solve the problem
problem.solve()

# Prepare output
quantities = [quantity[k].varValue for k in range(K)]
output = {"quantity": quantities}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')