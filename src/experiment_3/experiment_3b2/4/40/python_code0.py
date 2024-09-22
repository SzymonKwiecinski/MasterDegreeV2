import pulp
import json

# Load data from JSON format
data = json.loads("{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}")

# Parameters from data
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

K = len(cost)  # Number of minerals

# Create the Linear Programming problem
problem = pulp.LpProblem("Steel_Manufacturing", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # amount of mineral k melted
m = pulp.LpVariable("m", lowBound=0)  # amount of Manganese added

# Objective Function
profit = sell_price * n_steel_quant - (pulp.lpSum(cost[k] * x[k] for k in range(K)) + mang_price * m + melt_price * n_steel_quant)
problem += profit, "Total Profit"

# Constraints
# Steel quantity constraint
problem += (pulp.lpSum(x[k] for k in range(K)) + m == n_steel_quant, "Steel_Quantity_Constraint")

# Manganese percentage constraint
problem += ((pulp.lpSum(contmn[k] * x[k] for k in range(K)) + 100 * m) / n_steel_quant >= mn_percent, "Manganese_Percentage_Constraint")

# Silicon percentage constraints
problem += (pulp.lpSum(contsi[k] * x[k] for k in range(K)) / n_steel_quant >= si_min, "Silicon_Min_Constraint")
problem += (pulp.lpSum(contsi[k] * x[k] for k in range(K)) / n_steel_quant <= si_max, "Silicon_Max_Constraint")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the results for amount of minerals and manganese
amount = [x[k].varValue for k in range(K)]
num_mang = m.varValue
print(f'Optimal amounts of minerals melted: {amount}')
print(f'Optimal amount of Manganese added: {num_mang}')