import pulp
import json

# Input data
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

# Preparing the problem
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
K = len(price)

# Define the LP problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Define decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)]), "Total_Cost"

# Constraints
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"
for m in range(len(target)):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_{m+1}_Constraint"

# Solve the problem
problem.solve()

# Extracting the results
amount_results = [amount[k].varValue for k in range(K)]

# Output results
output = {
    "amount": amount_results
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')