import pulp
import json

# Input data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 
        'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}

# Extract variables
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

# Problem definition
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision variables
K = len(cost)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0, cat='Continuous')
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = (sell_price * n_steel_quant) - pulp.lpSum((cost[k] + melt_price) * (amount[k] / 1000) for k in range(K)) - mang_price * num_mang
problem += profit

# Constraints
# Total steel weight
problem += pulp.lpSum(amount[k] for k in range(K)) + num_mang == n_steel_quant

# Manganese content constraint
problem += (pulp.lpSum(contmn[k] * (amount[k] / 1000) for k in range(K)) + num_mang) / n_steel_quant >= mn_percent

# Silicon content constraints
silicon_content = pulp.lpSum(contsi[k] * (amount[k] / 1000) for k in range(K))
problem += silicon_content / n_steel_quant >= si_min
problem += silicon_content / n_steel_quant <= si_max

# Solve the problem
problem.solve()

# Results
amount_result = [amount[k].varValue for k in range(K)]
num_mang_result = num_mang.varValue

# Output
output = {
    "amount": amount_result,
    "num_mang": num_mang_result
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')