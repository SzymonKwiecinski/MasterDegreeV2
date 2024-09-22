import pulp
import json

# Data in JSON format
data_json = '{"n_steel_quant": 1000, "mn_percent": 0.45, "si_min": 3.25, "si_max": 5.0, "contsi": [4.0, 1.0, 0.6], "contmn": [0.45, 0.5, 0.4], "mang_price": 8.0, "cost": [21, 25, 15], "sell_price": 0.45, "melt_price": 0.005}'
data = json.loads(data_json)

# Variables
K = len(data['contsi'])
sell_price = data['sell_price']
n_steel_quant = data['n_steel_quant']
mang_price = data['mang_price']
melt_price = data['melt_price']
cost = data['cost']
contmn = data['contmn']
contsi = data['contsi']
mn_percent = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]
y = pulp.LpVariable('y', lowBound=0)

# Objective Function
problem += (sell_price * n_steel_quant 
             - pulp.lpSum((cost[k] / 1000) * x[k] for k in range(K))
             - mang_price * y 
             - melt_price * n_steel_quant), "Total Profit"

# Constraints
problem += (pulp.lpSum(x[k] for k in range(K)) + y == n_steel_quant, "Balance_Constraint")
problem += ((pulp.lpSum(contmn[k] * x[k] for k in range(K)) + y) / n_steel_quant >= mn_percent / 100, "Manganese_Constraint")
problem += (si_min / 100 * n_steel_quant <= pulp.lpSum(contsi[k] * x[k] for k in range(K)), "Silicon_Constraint_Min")
problem += (pulp.lpSum(contsi[k] * x[k] for k in range(K)) <= si_max / 100 * n_steel_quant, "Silicon_Constraint_Max")

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')