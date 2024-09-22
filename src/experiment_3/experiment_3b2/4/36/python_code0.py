import pulp
import json

# Given data as a JSON string
data = '''{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}'''
data = json.loads(data.replace("'", "\""))  # Convert to proper JSON format

# Extract data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)
M = len(target)

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Alloy_Quantity", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Alloy_Weight"

for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == alloy_quant * target[m], f"Metal_Composition_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')