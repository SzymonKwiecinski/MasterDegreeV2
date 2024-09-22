import pulp
import json

# Given data in JSON format
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

# Load data
data = json.loads(data_json)

# Variables
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

# Create the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0, cat='Continuous')
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

# Objective function
profit = (
    n_steel_quant * sell_price 
    - pulp.lpSum((cost[k] + melt_price) * (amount[k] / 1000) for k in range(K))
    - num_mang * mang_price
)
problem += profit

# Constraints
# Manganese content constraint
problem += (
    pulp.lpSum(amount[k] * contmn[k] for k in range(K)) + num_mang
    >= mn_percent * n_steel_quant
)

# Silicon content constraints
problem += (
    pulp.lpSum(amount[k] * contsi[k] for k in range(K)) >= si_min * n_steel_quant
)
problem += (
    pulp.lpSum(amount[k] * contsi[k] for k in range(K)) <= si_max * n_steel_quant
)

# Solve the problem
problem.solve()

# Extract results
result_amounts = [amount[k].varValue for k in range(K)]
result_num_mang = num_mang.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Amount of minerals (amount_k): {result_amounts}')
print(f'Total amount of Manganese added (num_mang): {result_num_mang}')