import pulp
import json

# Data input
data_json = '''{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}'''
data = json.loads(data_json)

# Problem parameters
A = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']
K = len(prices)
M = len(targets)

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K))

# Constraints
# Total weight of alloys equals A
problem += pulp.lpSum(x[k] for k in range(K)) == A

# Each metal's target quantity constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) == targets[m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')