import pulp
import json

# Load data from JSON format
data = json.loads('{"n_steel_quant": 1000, "mn_percent": 0.45, "si_min": 3.25, "si_max": 5.0, "contsi": [4.0, 1.0, 0.6], "contmn": [0.45, 0.5, 0.4], "mang_price": 8.0, "cost": [21, 25, 15], "sell_price": 0.45, "melt_price": 0.005}')

# Model parameters
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

# Number of minerals
K = len(cost)

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts('x', range(K), lowBound=0)  # Amount of mineral k melted
y = pulp.LpVariable('y', lowBound=0)  # Amount of Manganese added

# Objective Function
profit = sell_price * n_steel_quant - pulp.lpSum(cost[k] * x[k] for k in range(K)) \
         - mang_price * y - melt_price * pulp.lpSum(x[k] for k in range(K))
problem += profit

# Constraints
problem += pulp.lpSum(x[k] for k in range(K)) + y == n_steel_quant  # Total steel
problem += (pulp.lpSum(contmn[k] * x[k] for k in range(K)) + y) / n_steel_quant >= mn_percent / 100  # Manganese percentage
problem += pulp.lpSum(contsi[k] * x[k] for k in range(K)) / n_steel_quant >= si_min / 100  # Minimum Silicon percentage
problem += pulp.lpSum(contsi[k] * x[k] for k in range(K)) / n_steel_quant <= si_max / 100  # Maximum Silicon percentage

# Solve the problem
problem.solve()

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')