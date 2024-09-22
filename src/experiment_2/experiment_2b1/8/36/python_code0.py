import pulp
import json

# Load data from JSON
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys
K = len(price)

# Create the problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Decision variables
amounts = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([price[k] * amounts[k] for k in range(K)]), "Total_Cost"

# Constraints
problem += pulp.lpSum([amounts[k] for k in range(K)]) == alloy_quant, "Total_Alloy_Quantity"

for m in range(len(target)):
    problem += pulp.lpSum([amounts[k] * ratio[k][m] for k in range(K)]) == target[m], f"Target_Metal_{m+1}"

# Solve the problem
problem.solve()

# Prepare the output
amount_solution = [amounts[k].varValue for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the amounts
output = {"amount": amount_solution}
print(output)