import pulp
import json

# Data from the provided JSON
data_json = '''{
    "n_steel_quant": 1000,
    "mn_percent": 0.45,
    "si_min": 3.25,
    "si_max": 5.0,
    "contsi": [4.0, 1.0, 0.6],
    "contmn": [0.45, 0.5, 0.4],
    "mang_price": 8.0,
    "cost": [21, 25, 15],
    "sell_price": 0.45,
    "melt_price": 0.005
}'''

data = json.loads(data_json)

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

K = len(contsi)  # Number of minerals

# Problem definition
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
amount_k = pulp.LpVariable.dicts("amount_k", range(K), lowBound=0)  # Amount of each mineral
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of manganese added

# Objective Function
profit = (sell_price - mang_price - melt_price - pulp.lpSum((cost[k] / 1000) * amount_k[k] for k in range(K))) * n_steel_quant
problem += profit, "Total_Profit"

# Constraints
# Silicon content constraint
problem += (pulp.lpSum(contsi[k] * amount_k[k] for k in range(K)) + (si_min / 100) * n_steel_quant <= n_steel_quant * si_max), "Silicon_Content_Constraint"

# Manganese content constraint
problem += (pulp.lpSum(contmn[k] * amount_k[k] for k in range(K)) + num_mang >= (mn_percent / 100) * n_steel_quant), "Manganese_Content_Constraint"

# Solve the problem
problem.solve()

# Output results
amounts = [amount_k[k].varValue for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Amounts of minerals melted: {amounts}')
print(f'Amount of manganese added: {num_mang.varValue}')