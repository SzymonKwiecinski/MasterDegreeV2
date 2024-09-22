import pulp
import json

# Data input
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 
        'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}

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

# Problem setup
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Variables
K = len(contsi)
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function
profit = (sell_price * n_steel_quant) - pulp.lpSum(cost[k] * amount[k] / 1000 + melt_price * amount[k] + mang_price * num_mang for k in range(K))
problem += profit

# Constraints
total_si = pulp.lpSum(contsi[k] * amount[k] for k in range(K))
total_mn = pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang

problem += (total_mn >= mn_percent * n_steel_quant)  # Manganese content
problem += (total_si / n_steel_quant >= si_min)      # Minimum Silicon content
problem += (total_si / n_steel_quant <= si_max)      # Maximum Silicon content

# Total amount constraint
problem += (pulp.lpSum(amount) == n_steel_quant)      # Total amount of minerals used

# Solve the problem
problem.solve()

# Output results
amount_values = [pulp.value(amount[k]) for k in range(K)]
num_mang_value = pulp.value(num_mang)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output format
output = {
    "amount": amount_values,
    "num_mang": num_mang_value
}

output