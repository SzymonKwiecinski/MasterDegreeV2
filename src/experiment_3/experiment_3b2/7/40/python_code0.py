import pulp
import json

# Data provided in JSON format
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
K = len(cost)

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Amount of mineral k used
y = pulp.LpVariable("y", lowBound=0)                  # Amount of manganese added

# Objective function
profit = n_steel_quant * sell_price - pulp.lpSum([x[k] * cost[k] for k in range(K)]) - y * mang_price - pulp.lpSum([x[k] * melt_price for k in range(K)])
problem += profit

# Constraints
# Total steel production
problem += pulp.lpSum([x[k] for k in range(K)]) + y == n_steel_quant, "SteelProduction"

# Manganese content
problem += pulp.lpSum([x[k] * (contmn[k] / 1000) for k in range(K)]) + y >= (mn_percent / 100) * n_steel_quant, "ManganeseContent"

# Silicon content
problem += (si_min / 100) * n_steel_quant <= pulp.lpSum([x[k] * (contsi[k] / 1000) for k in range(K)]) <= (si_max / 100) * n_steel_quant, "SiliconContent"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')