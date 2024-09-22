import pulp
import json

# Data input
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 
        'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}

# Variables
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

K = len(contsi)  # Number of minerals

# Create the LP problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Amount of each mineral melted
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of Manganese added

# Objective function: maximize profit
profit = sell_price * n_steel_quant - pulp.lpSum((cost[k] * amount[k] / 1000) + (melt_price * amount[k]) for k in range(K)) - (mang_price * num_mang)
problem += profit

# Constraints
problem += pulp.lpSum(amount[k] * contsi[k] for k in range(K)) + num_mang * 0 >= n_steel_quant * si_min, "min_si"
problem += pulp.lpSum(amount[k] * contsi[k] for k in range(K)) + num_mang * 0 <= n_steel_quant * si_max, "max_si"
problem += pulp.lpSum(amount[k] * contmn[k] for k in range(K)) + num_mang >= n_steel_quant * mn_percent, "min_mn"

# Solve the problem
problem.solve()

# Output
amount_values = [amount[k].varValue for k in range(K)]
num_mang_value = num_mang.varValue

result = {
    "amount": amount_values,
    "num_mang": num_mang_value
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')