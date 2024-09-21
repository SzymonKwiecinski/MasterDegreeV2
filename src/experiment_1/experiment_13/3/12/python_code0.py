import pulp
import json

# Data provided in JSON format
data_json = '''{
    "alloy_quant": 1000,
    "target": [300, 700],
    "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    "price": [5, 4, 3, 2, 1.5]
}'''

# Load the data
data = json.loads(data_json)

# Define parameters from data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys (K) and components (M)
K = len(price)
M = len(target)

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraint for total alloy quantity
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"

# Constraints for target components
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) >= target[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')