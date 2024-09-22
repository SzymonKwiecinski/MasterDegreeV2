import pulp

# Parsing the data
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

# Problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(len(contsi))]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective Function
profit = sell_price * n_steel_quant - sum((cost[k]/1000) * amount[k] for k in range(len(contsi))) \
         - mang_price * num_mang - melt_price * sum(amount[k] for k in range(len(contsi)))

problem += profit

# Constraints
# Mn content constraint
problem += sum(amount[k] * (contmn[k]/100) for k in range(len(contmn))) + num_mang >= (mn_percent/100) * n_steel_quant

# Si content constraint
problem += si_min * n_steel_quant <= sum(amount[k] * (contsi[k]/100) for k in range(len(contsi)))
problem += sum(amount[k] * (contsi[k]/100) for k in range(len(contsi))) <= si_max * n_steel_quant

# Total quantity constraint
problem += sum(amount) + num_mang == n_steel_quant

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')