import json
import pulp

# Input data
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], 
                  [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Extracting data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
num_alloys = len(price)
num_metals = len(target)

# Create the Linear Programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables for the amount of each alloy
amounts = pulp.LpVariable.dicts("Amount", range(num_alloys), lowBound=0)

# Objective function: Minimize the total cost
problem += pulp.lpSum([amounts[k] * price[k] for k in range(num_alloys)])

# Constraints for the target quantities of each metal
for m in range(num_metals):
    problem += (pulp.lpSum([amounts[k] * ratio[k][m] for k in range(num_alloys)]) == target[m]), f"Metal_{m+1}_requirement")

# Constraint for the total amount of alloy produced
problem += (pulp.lpSum([amounts[k] for k in range(num_alloys)]) == alloy_quant, "Total_alloy_quantity")

# Solve the problem
problem.solve()

# Prepare the output
amount_result = [amounts[k].varValue for k in range(num_alloys)]

# Print the result along with the objective value
print(json.dumps({"amount": amount_result}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')