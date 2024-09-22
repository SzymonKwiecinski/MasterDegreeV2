import pulp
import json

# Data
data_json = '''{
    "alloy_quant": 1000, 
    "target": [300, 700], 
    "ratio": [
        [0.1, 0.9], 
        [0.25, 0.75], 
        [0.5, 0.5], 
        [0.75, 0.25], 
        [0.95, 0.05]
    ], 
    "price": [5, 4, 3, 2, 1.5]
}'''

data = json.loads(data_json)

# Extracting parameters from data
A = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']
M = len(targets)
K = len(prices)

# Creating the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K))

# Constraints
# Constraint to match total alloy weight
problem += pulp.lpSum(x[k] for k in range(K)) == A

# Constraints for each metal target
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) == targets[m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')