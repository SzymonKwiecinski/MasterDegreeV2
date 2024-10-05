import pulp

# Data input
data = {
    'n_steel_quant': 1000,
    'mn_percent': 0.45,
    'si_min': 3.25,
    'si_max': 5.0,
    'contsi': [4.0, 1.0, 0.6],
    'contmn': [0.45, 0.5, 0.4],
    'mang_price': 8.0,
    'cost': [21, 25, 15],
    'sell_price': 0.45,
    'melt_price': 0.005
}

# Extracting data
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

# Define the problem
problem = pulp.LpProblem("Steel_Manufacturing", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function: Maximize profit
profit_per_ton = sell_price - melt_price
total_cost = (pulp.lpSum(cost[k] * amount[k] for k in range(K)) / 1000) + mang_price * num_mang
problem += (profit_per_ton * n_steel_quant - total_cost)

# Constraints

# Total weight constraint
problem += (pulp.lpSum(amount) == n_steel_quant)

# Manganese content constraint
problem += (pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang >= mn_percent * n_steel_quant)

# Silicon content constraint
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K)) >= si_min * n_steel_quant)
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant)

# Solve the problem
problem.solve()

# Output the results
amount_values = [pulp.value(amount[k]) for k in range(K)]
num_mang_value = pulp.value(num_mang)

output = {
    "amount": amount_values,
    "num_mang": [num_mang_value]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')