import pulp
import json

# Data input (as provided)
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 
        'mang_price': 8.0, 'cost': [21, 25, 15], 
        'sell_price': 0.45, 'melt_price': 0.005}

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

# Number of minerals
K = len(contsi)

# Define the problem
problem = pulp.LpProblem("Steel_Manufacturing_Profit_Maximization", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function: maximize profit
profit = (sell_price * n_steel_quant) - (sum(cost[k] * amount[k] / 1000 for k in range(K)) + 
                                            melt_price * (sum(amount) + num_mang) + 
                                            mang_price * num_mang)
problem += profit

# Constraints
# Total weight of the steel must exactly equal n_steel_quant
problem += pulp.lpSum(amount[k] * (contmn[k] / 100) for k in range(K)) + num_mang >= mn_percent * n_steel_quant
problem += pulp.lpSum(amount[k] * (contsi[k] / 100) for k in range(K)) >= si_min * n_steel_quant
problem += pulp.lpSum(amount[k] * (contsi[k] / 100) for k in range(K)) <= si_max * n_steel_quant

# Solve the problem
problem.solve()

# Output the results
amount_values = [pulp.value(amount[k]) for k in range(K)]
num_mang_value = pulp.value(num_mang)

output = {
    "amount": amount_values,
    "num_mang": num_mang_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')