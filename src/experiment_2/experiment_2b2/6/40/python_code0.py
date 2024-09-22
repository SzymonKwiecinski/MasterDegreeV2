import pulp

# Data provided in JSON format
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

K = len(contsi)  # Number of minerals

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective Function: Maximize profit
problem += (
    pulp.lpSum((sell_price - cost[k] / 1000 - melt_price) * amount[k] for k in range(K)) +
    (sell_price - mang_price) * num_mang
)

# Constraints
# Total steel quantity constraint
problem += pulp.lpSum(amount) + num_mang == n_steel_quant

# Manganese percentage constraint
problem += (
    pulp.lpSum(contmn[k] * amount[k] / 100 for k in range(K)) +
    num_mang / n_steel_quant
) >= mn_percent * n_steel_quant / 100

# Silicon percentage constraint (minimum)
problem += (
    pulp.lpSum(contsi[k] * amount[k] for k in range(K))
) >= si_min * pulp.lpSum(amount)

# Silicon percentage constraint (maximum)
problem += (
    pulp.lpSum(contsi[k] * amount[k] for k in range(K))
) <= si_max * pulp.lpSum(amount)

# Solve the problem
problem.solve()

# Result extraction
result_amount = [pulp.value(amount[k]) for k in range(K)]
result_num_mang = pulp.value(num_mang)

result = {
    "amount": result_amount,
    "num_mang": result_num_mang
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')