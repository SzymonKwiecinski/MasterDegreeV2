import pulp
import json

# Data input
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Extract data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)
M = len(target)

# Create the problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("alloy", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(price[k] * x[k] for k in range(K))

# Constraints
# Total amount of alloy produced must be equal to the required amount
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant

# Proportional constraints for each metal
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m] * alloy_quant

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')