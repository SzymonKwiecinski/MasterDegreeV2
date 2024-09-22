import pulp
import json

# Input data
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Extracting data from the input
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)
M = len(target)

# Define the problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Define decision variables
amounts = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * amounts[k] for k in range(K)), "Total Cost"

# Constraints
problem += pulp.lpSum(amounts[k] for k in range(K)) == alloy_quant, "Total Alloy Quantity"
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amounts[k] for k in range(K)) == target[m], f"Metal_{m+1}_Target"

# Solve the problem
problem.solve()

# Output the results
amount_output = [amounts[k].varValue for k in range(K)]
print(json.dumps({"amount": amount_output}))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')