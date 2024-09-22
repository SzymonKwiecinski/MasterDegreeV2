import pulp
import json

# Data input
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Extracting data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of metals and products
M = len(target)
K = len(price)

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([price[k] * x[k] for k in range(K)]), "Total_Cost"

# Total weight constraint
problem += pulp.lpSum([x[k] for k in range(K)]) == alloy_quant, "Total_Weight"

# Metal composition constraints
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * x[k] for k in range(K)]) == target[m] * alloy_quant, f"Metal_Composition_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')