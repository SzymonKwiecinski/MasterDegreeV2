import pulp
import json

data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], 
                  [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Extract data from the JSON
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Define decision variables
amount = pulp.LpVariable.dicts("amount", range(len(ratio)), lowBound=0)

# Objective function: minimize total cost
problem += pulp.lpSum([amount[k] * price[k] for k in range(len(price))]), "Total_Cost"

# Constraints
problem += pulp.lpSum([amount[k] for k in range(len(ratio))]) == alloy_quant, "Total_Amount"

# Add constraints for each metal
for m in range(len(target)):
    problem += pulp.lpSum([amount[k] * ratio[k][m] for k in range(len(ratio))]) == target[m], f"Target_Metal_{m+1}"

# Solve the problem
problem.solve()

# Prepare output
amount_solution = [amount[k].varValue for k in range(len(ratio))]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the amounts
output = {
    "amount": amount_solution
}

print(output)