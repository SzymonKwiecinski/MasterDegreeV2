import pulp
import json

# Input data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0,
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4],
        'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45,
        'melt_price': 0.005}

# Problem parameters
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
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Mineral amounts
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of manganese added

# Objective Function
profit = (sell_price * n_steel_quant) - (melt_price * pulp.lpSum(amount[k] for k in range(K))) - (mang_price * num_mang)
problem += profit

# Constraints
# Total weight of Steel
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) / n_steel_quant >= si_min
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) / n_steel_quant <= si_max

# Manganese Constraint
problem += (pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang) / n_steel_quant >= mn_percent

# Solve the problem
problem.solve()

# Collect results
amount_values = [amount[k].varValue for k in range(K)]
num_mang_value = num_mang.varValue

# Output the result
result = {
    "amount": amount_values,
    "num_mang": num_mang_value
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')