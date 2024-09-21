import pulp
import json

# Data
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Constants
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)   # Number of alloys
M = len(target)  # Number of components

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("AlloyQuantity", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"

# Constraint 2: Component requirements
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) >= target[m], f"Target_Component_{m + 1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')