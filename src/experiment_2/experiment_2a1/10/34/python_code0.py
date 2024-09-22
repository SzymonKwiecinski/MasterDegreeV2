import pulp
import json

data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting data from the input
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(prices)
M = len(demands)

# Create the linear programming problem
problem = pulp.LpProblem("Food_Purchase_Problem", pulp.LpMinimize)

# Create decision variables for the quantity of each food
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function: Minimize total price
problem += pulp.lpSum(prices[k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints: Ensure each nutrient meets the demand
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demands[m], f"Nutrient_Requirement_{m}"

# Solve the problem
problem.solve()

# Collect the results
quantity_solution = [quantity[k].varValue for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Prepare the output in the required format
output = {"quantity": quantity_solution}
print(json.dumps(output))