import pulp

# Data
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

# Define the problem
problem = pulp.LpProblem("Steel_Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function: maximize profit
revenue = sell_price * n_steel_quant
cost_minerals = pulp.lpSum([(cost[k] / 1000 + melt_price) * amount[k] for k in range(K)])
cost_manganese = num_mang * mang_price
profit = revenue - cost_minerals - cost_manganese
problem += profit

# Constraints
# Ensure total steel quantity
problem += pulp.lpSum(amount) == n_steel_quant - num_mang

# Manganese content
problem += (pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang) >= mn_percent * n_steel_quant

# Silicon content
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) >= si_min * n_steel_quant
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant

# Solve the problem
problem.solve()

# Output results
result = {
    "amount": [amount[k].varValue for k in range(K)],
    "num_mang": num_mang.varValue
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')