import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Create the LP problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Variables
K = len(data['price'])  # Number of food items
quantities = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(data['price'][k] * quantities[k] for k in range(K)), "Total_Cost"

# Constraints: Ensure that each nutrient demand is met
M = len(data['demand'])  # Number of nutrients
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantities[k] for k in range(K)) >= data['demand'][m], f"Nutrient_Requirement_{m}"

# Solve the problem
problem.solve()

# Get the quantities of each food
quantity = [quantities[k].varValue for k in range(K)]

# Print the output
output = {
    "quantity": quantity
}
print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')