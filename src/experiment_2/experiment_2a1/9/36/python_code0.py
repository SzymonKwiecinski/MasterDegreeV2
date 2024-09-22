import pulp
import json

# Input data
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

# Extracting parameters from data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
num_alloys = len(price)
num_metals = len(target)

# Create a linear programming problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Decision variables for the amount of each alloy
amounts = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(num_alloys)]

# Objective function: Minimize the total cost
problem += pulp.lpSum(price[k] * amounts[k] for k in range(num_alloys)), "Total_Cost"

# Constraints
# Total amount of alloys must equal the desired alloy quantity
problem += pulp.lpSum(amounts) == alloy_quant, "Total_Alloy_Quantity"

# Constraints for each metal's target quantity
for m in range(num_metals):
    problem += pulp.lpSum(ratio[k][m] * amounts[k] for k in range(num_alloys)) == target[m], f"Metal_{m+1}_Target"

# Solve the problem
problem.solve()

# Prepare output
amounts_result = [amounts[k].varValue for k in range(num_alloys)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the amounts of each alloy needed
output = {"amount": amounts_result}
print(json.dumps(output))