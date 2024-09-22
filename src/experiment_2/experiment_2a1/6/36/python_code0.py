import pulp
import json

data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

# Extract data from JSON
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Define the problem
problem = pulp.LpProblem('Alloy_Production', pulp.LpMinimize)

# Define decision variables for amounts of each alloy
K = len(price)  # Number of alloys
amounts = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function: minimize the total cost
problem += pulp.lpSum(price[k] * amounts[k] for k in range(K)), "Total Cost"

# Constraints
# 1. The total weight of the selected alloys should equal alloy_quant
problem += pulp.lpSum(amounts[k] for k in range(K)) == alloy_quant, "Total Weight"

# 2. The target weight for each metal
for m in range(len(target)):
    problem += pulp.lpSum(ratio[k][m] * amounts[k] for k in range(K)) == target[m], f"Target_Metal_{m+1}"

# Solve the problem
problem.solve()

# Prepare the amounts for output
amounts_result = [amounts[k].varValue for k in range(K)]

output = {"amount": amounts_result}
print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')