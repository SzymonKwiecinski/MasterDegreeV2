import pulp

# Data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 
        'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}

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

K = len(contsi)

# Initialize LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function
revenue = sell_price * n_steel_quant
mineral_cost = pulp.lpSum((cost[k] / 1000.0) * amount[k] for k in range(K))
mang_cost = mang_price * num_mang
melt_cost = melt_price * pulp.lpSum(amount[k] for k in range(K))

problem += revenue - (mineral_cost + mang_cost + melt_cost), "Profit"

# Constraints
problem += pulp.lpSum(amount[k] for k in range(K)) == n_steel_quant, "Total_Steel_Quantity"
problem += pulp.lpSum(amount[k] * contmn[k] / 100.0 for k in range(K)) + num_mang >= mn_percent * n_steel_quant / 100.0, "Mn_Content"
problem += pulp.lpSum(amount[k] * contsi[k] / 100.0 for k in range(K)) >= si_min * n_steel_quant / 100.0, "Si_Min_Content"
problem += pulp.lpSum(amount[k] * contsi[k] / 100.0 for k in range(K)) <= si_max * n_steel_quant / 100.0, "Si_Max_Content"

# Solve
problem.solve()

# Output
output = {
    "amount": [amount[k].varValue for k in range(K)],
    "num_mang": num_mang.varValue
}

print(output)

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')