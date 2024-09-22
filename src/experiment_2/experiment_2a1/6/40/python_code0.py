import pulp
import json

# Input data
data = json.loads("{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}")

# Parameters
n_steel_quant = data['n_steel_quant']
mn_percent = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
costs = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']

# Create a LP problem
problem = pulp.LpProblem("Steel_Manufacturing", pulp.LpMaximize)

# Decision variables
K = len(contsi)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # amount of each mineral melted
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # amount of Manganese added

# Objective function: Maximize profit
profit = sell_price * n_steel_quant - (melt_price * sum(amount[k] for k in range(K)) + mang_price * num_mang)
problem += profit

# Constraints
# Total steel production
problem += sum(amount[k] * (contsi[k] / 100) for k in range(K)) + (num_mang / 100) >= n_steel_quant * si_min, "Si_Min_Constraint"
problem += sum(amount[k] * (contsi[k] / 100) for k in range(K)) + (num_mang / 100) <= n_steel_quant * si_max, "Si_Max_Constraint"

# Manganese content
problem += (sum(amount[k] * (contmn[k] / 100) for k in range(K)) + num_mang) >= n_steel_quant * mn_percent, "Mn_Constraint"

# Solve the problem
problem.solve()

# Collect results
amount_values = [amount[k].varValue for k in range(K)]
num_mang_value = num_mang.varValue

# Output results
output = {
    "amount": amount_values,
    "num_mang": num_mang_value
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')