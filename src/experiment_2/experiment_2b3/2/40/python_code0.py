import pulp

# Parse the input data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 
        'mang_price': 8.0, 'cost': [21, 25, 15], 
        'sell_price': 0.45, 'melt_price': 0.005}

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

K = len(contsi)

# Define the LP problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Define the variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective Function: Maximize Profit
revenue = sell_price * n_steel_quant
total_cost_minerals = pulp.lpSum((cost[k] / 1000 + melt_price) * amount[k] for k in range(K))
total_cost_manganese = mang_price * num_mang
total_material_cost = total_cost_minerals + total_cost_manganese

profit = revenue - total_material_cost
problem += profit

# Constraints
# Total weight of steel produced
problem += pulp.lpSum(amount[k] for k in range(K)) + num_mang == n_steel_quant

# Manganese content constraint
problem += pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang >= mn_percent * n_steel_quant

# Silicon content constraint
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) >= si_min * n_steel_quant
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant

# Solve the problem
problem.solve()

# Extract the results
amount_values = [pulp.value(amount[k]) for k in range(K)]
num_mang_value = pulp.value(num_mang)

# Output format
output = {
    "amount": amount_values,
    "num_mang": [num_mang_value]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')