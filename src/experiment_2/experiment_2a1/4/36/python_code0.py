import pulp
import json

data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Extract data from the JSON
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Initialize the problem
problem = pulp.LpProblem("Alloy_Cost_Minimization", pulp.LpMinimize)

# Define variables
K = len(price)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function: Minimize cost
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)]), "Total_Cost"

# Constraints
problem += pulp.lpSum([amount[k] for k in range(K)]) == alloy_quant, "Total_Alloy_Quantity"
for m in range(len(target)):
    problem += pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) == target[m], f"Metal_{m+1}_Target"

# Solve the problem
problem.solve()

# Prepare output
output = {"amount": [amount[k].varValue for k in range(K)]}
print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')