import pulp
import json

# Data input
data_json = '''{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}'''
data = json.loads(data_json)

# Extracting data from JSON
A = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of metals and alloys
M = len(target)
K = len(price)

# Create the LP problem
problem = pulp.LpProblem("AlloyProduction", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "TotalCost"

# Constraints
problem += pulp.lpSum(x[k] for k in range(K)) == A, "TotalWeight"

for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"MetalRequirement_{m+1}"

# Solve the problem
problem.solve()

# Output the results
amounts = [x[k].varValue for k in range(K)]
print(f'Amounts to purchase: {amounts}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')