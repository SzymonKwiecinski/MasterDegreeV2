import pulp
import json

# Data from the provided JSON
data = json.loads('{"n_steel_quant": 1000, "mn_percent": 0.45, "si_min": 3.25, "si_max": 5.0, "contsi": [4.0, 1.0, 0.6], "contmn": [0.45, 0.5, 0.4], "mang_price": 8.0, "cost": [21, 25, 15], "sell_price": 0.45, "melt_price": 0.005}')

# Parameters
n_steel_quant = data['n_steel_quant']
mn_percent = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']

# Number of materials
K = len(cost)

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Amount of each material
M = pulp.LpVariable("M", lowBound=0)                  # Amount of manganese

# Objective function
profit = (sell_price * n_steel_quant) - (pulp.lpSum([cost[k] / 1000 * x[k] for k in range(K)]) + mang_price * M + melt_price * pulp.lpSum([x[k] for k in range(K)]))
problem += profit

# Constraints
# Steel Quantity Constraint
problem += (pulp.lpSum([x[k] for k in range(K)]) + M == n_steel_quant)

# Manganese Content Constraint
problem += (pulp.lpSum([contmn[k] * x[k] for k in range(K)]) + M >= (mn_percent / 100) * n_steel_quant)

# Silicon Content Constraints
problem += (pulp.lpSum([contsi[k] * x[k] for k in range(K)]) >= (si_min / 100) * n_steel_quant)
problem += (pulp.lpSum([contsi[k] * x[k] for k in range(K)]) <= (si_max / 100) * n_steel_quant)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')