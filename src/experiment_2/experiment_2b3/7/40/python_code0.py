import pulp

# Parse the input data
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

# Number of minerals
K = len(contsi)

# Define the LP problem
problem = pulp.LpProblem("Steel_Production_Max_Profit", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f"amount_{k}", lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Objective Function: Maximize profit
profit = (sell_price * n_steel_quant) - (pulp.lpSum((cost[k] * amount[k] / 1000) for k in range(K)) + melt_price * n_steel_quant + mang_price * num_mang)
problem += profit

# Constraints

# Total quantity of steel produced
problem += (pulp.lpSum(amount) + num_mang == n_steel_quant), "Total_Steel_Production"

# Manganese content constraint
problem += (pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang >= mn_percent * n_steel_quant), "Mn_Content"

# Silicon content constraints
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K)) >= si_min * n_steel_quant), "Si_Min_Content"
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant), "Si_Max_Content"

# Solve the problem
problem.solve()

# Construct the result
result = {
    "amount": [pulp.value(amount[k]) for k in range(K)],
    "num_mang": [pulp.value(num_mang)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')