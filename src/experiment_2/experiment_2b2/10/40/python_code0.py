import pulp

# Parse the data
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

# Defining constants
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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables: amount of each mineral melted and amount of Mn added
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function: maximize profit
profit = (sell_price * n_steel_quant 
          - pulp.lpSum([(cost[k] * amount[k])/1000 + melt_price * amount[k] for k in range(K)]) 
          - num_mang * mang_price)
problem += profit

# Constraints

# Total steel constraint
problem += (pulp.lpSum(amount) + num_mang == n_steel_quant)

# Manganese content constraint
problem += (pulp.lpSum([contmn[k] * amount[k]/100 for k in range(K)]) + num_mang >= mn_percent * n_steel_quant / 100)

# Silicon content constraints
problem += (pulp.lpSum([contsi[k] * amount[k]/100 for k in range(K)]) >= si_min * n_steel_quant / 100)
problem += (pulp.lpSum([contsi[k] * amount[k]/100 for k in range(K)]) <= si_max * n_steel_quant / 100)

# Solving the problem
problem.solve()

# Collecting results
result_amount = [pulp.value(amount[k]) for k in range(K)]
result_num_mang = pulp.value(num_mang)

# Print the results
output = {
    "amount": result_amount,
    "num_mang": result_num_mang
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')