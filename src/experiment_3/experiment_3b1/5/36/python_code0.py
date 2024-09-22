import pulp
import json

# Data input
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Parameters
A = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

M = len(targets)  # Number of metals
K = len(prices)   # Number of alloys

# Create the linear programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', range(K), lowBound=0)  # Amount of alloy k purchased

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
problem += pulp.lpSum(x[k] for k in range(K)) == A, "Total_Alloy_Quantity"

for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) == targets[m], f"Metal_Requirement_{m+1}"

# Solve the problem
problem.solve()

# Output the results
amounts = [pulp.value(x[k]) for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Amounts of alloys purchased: {amounts}')