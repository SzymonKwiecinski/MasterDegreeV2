import pulp
import json

# Input data
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Extract data from input
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Define the problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Define decision variables
K = len(price)  # number of alloys
amounts = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * amounts[k] for k in range(K))

# Constraints
for m in range(len(target)):
    problem += pulp.lpSum(ratio[k][m] * amounts[k] for k in range(K)) == target[m], f"TargetMetal{m}"

# Total amount constraint
problem += pulp.lpSum(amounts[k] for k in range(K)) == alloy_quant, "TotalAlloyAmount"

# Solve the problem
problem.solve()

# Output the results
amount_result = [amounts[k].varValue for k in range(K)]
output = {"amount": amount_result}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')