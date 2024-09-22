import pulp
import json

# Load data from the provided JSON string
data = json.loads("{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}")

# Extract data
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

# Create the Linear Programming problem
problem = pulp.LpProblem("Steel_Production_Profit", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective Function
profit = (sell_price * n_steel_quant) - (pulp.lpSum(cost[k] * amount[k] / 1000 + melt_price * amount[k] for k in range(K)) + mang_price * num_mang)
problem += profit

# Constraints

# Manganese Content Constraint
problem += (pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang) >= (mn_percent / 100) * n_steel_quant

# Silicon Content Constraints
problem += (si_min * n_steel_quant) <= (pulp.lpSum(contsi[k] * amount[k] for k in range(K)))
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K))) <= (si_max * n_steel_quant)

# Total Steel Requirement
problem += pulp.lpSum(amount) + num_mang == n_steel_quant

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')