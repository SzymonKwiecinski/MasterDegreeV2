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
K = len(contsi)  # Total number of minerals

# Create the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Amount of mineral k melted
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of Manganese added

# Objective Function
profit = (sell_price * n_steel_quant) - (
    pulp.lpSum((cost[k] / 1000) * amount[k] + melt_price * amount[k] for k in range(K)) +
    mang_price * num_mang)

problem += profit

# Constraints
# 1. Total amount of steel produced
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K)) + num_mang >= (mn_percent / 100) * n_steel_quant)

# 2. Silicon content constraints
problem += (si_min * n_steel_quant <= pulp.lpSum(contsi[k] * amount[k] for k in range(K)))
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')