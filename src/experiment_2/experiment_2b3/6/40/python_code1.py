import pulp

# Data received
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

# Problem data
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

# Create the LP problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function: maximize profit
total_cost_minerals = pulp.lpSum([cost[k] * amount[k] / 1000 for k in range(K)])
total_cost_melting = pulp.lpSum([melt_price * amount[k] for k in range(K)])
total_cost_manganese = mang_price * num_mang

revenue = sell_price * n_steel_quant

profit = revenue - (total_cost_minerals + total_cost_melting + total_cost_manganese)
problem += profit

# Constraints
# Total weight constraint
problem += pulp.lpSum(amount) + num_mang == n_steel_quant

# Manganese content constraint
problem += pulp.lpSum([contmn[k] * amount[k] for k in range(K)]) + num_mang >= mn_percent * n_steel_quant

# Silicon content constraints
problem += pulp.lpSum([contsi[k] * amount[k] for k in range(K)]) >= si_min * n_steel_quant
problem += pulp.lpSum([contsi[k] * amount[k] for k in range(K)]) <= si_max * n_steel_quant

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "amount": [pulp.value(amount[k]) for k in range(K)],
    "num_mang": pulp.value(num_mang)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')