import pulp
import json

# Input data
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Extracting data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)  # Number of alloys
M = len(target)  # Number of metals

# Create the problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Decision variables
amounts = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([price[k] * amounts[k] for k in range(K)])

# Constraints
problem += pulp.lpSum([amounts[k] for k in range(K)]) == alloy_quant  # Total weight of alloys must equal alloy_quant

# Each metal's target constraint
for m in range(M):
    problem += pulp.lpSum([ratios[m] * amounts[k] for k in range(K)]) == target[m] for ratios in ratio

# Solve the problem
problem.solve()

# Output the amounts
amount = [amounts[k].varValue for k in range(K)]
print(json.dumps({"amount": amount}))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')