import pulp
import json

# Input data
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

# Define the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Number of minerals
K = len(contsi)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # amounts of each mineral
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # amount of manganese added

# Objective function: Profit = Revenue - Costs
revenue = sell_price * n_steel_quant
costs = pulp.lpSum((amount[k] * cost[k] * 0.001 + melt_price * n_steel_quant) for k in range(K)) + (num_mang * mang_price)
profit = revenue - costs

problem += profit  # Maximize profit

# Constraints
# Total manganese content constraint
problem += pulp.lpSum((num_mang + pulp.lpSum(amount[k] * contmn[k] * 0.01 for k in range(K))) / n_steel_quant) >= mn_percent

# Total silicon content constraints
total_si_content = pulp.lpSum(pulp.lpSum(amount[k] * contsi[k] * 0.01 for k in range(K))) / n_steel_quant
problem += total_si_content >= si_min
problem += total_si_content <= si_max

# Total weight constraint
problem += pulp.lpSum(amount[k] for k in range(K)) + num_mang == n_steel_quant

# Solve the problem
problem.solve()

# Output results
amount_values = [amount[k].varValue for k in range(K)]
num_mang_value = num_mang.varValue

result = {
    "amount": amount_values,
    "num_mang": num_mang_value
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')