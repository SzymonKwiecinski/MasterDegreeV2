import pulp
import json

# Data
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Parameters
alloy_quantity = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # Number of alloys
M = len(target)  # Number of components

# Create the problem variable
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum([price[k] * x[k] for k in range(K)]), "Total_Cost"

# Constraint: Total quantity of alloys produced
problem += pulp.lpSum([x[k] for k in range(K)]) == alloy_quantity, "Total_Alloy_Quantity"

# Constraints: Quantity of each target component in the alloy
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * x[k] for k in range(K)]) >= target[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for k in range(K):
    print(f'Quantity of alloy {k}: {x[k].varValue}')