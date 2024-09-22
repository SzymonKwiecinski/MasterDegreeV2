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

# Constants
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

# Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Constraints
total_steel = pulp.lpSum(amount) + num_mang == n_steel_quant
mn_constraint = (
    pulp.lpSum([amount[k] * contmn[k] for k in range(K)]) + num_mang
    >= mn_percent * n_steel_quant
)
si_min_constraint = (
    pulp.lpSum([amount[k] * contsi[k] for k in range(K)]) 
    >= si_min * n_steel_quant
)
si_max_constraint = (
    pulp.lpSum([amount[k] * contsi[k] for k in range(K)]) 
    <= si_max * n_steel_quant
)

problem += total_steel
problem += mn_constraint
problem += si_min_constraint
problem += si_max_constraint

# Objective
revenue = sell_price * n_steel_quant
mang_cost = mang_price * num_mang
mineral_cost = pulp.lpSum(
    [(amount[k] * cost[k] / 1000.0 + amount[k] * melt_price) for k in range(K)]
)

profit = revenue - mang_cost - mineral_cost
problem += profit

# Solve
problem.solve()

# Results
result = {
    "amount": [amount[k].varValue for k in range(K)],
    "num_mang": [num_mang.varValue]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')