import pulp
import json

# Data parsed from the provided JSON format
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

# Parameter setup
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
K = len(cost)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Production levels for each steel type
y = pulp.LpVariable("y", lowBound=0)  # Manganese addition

# Objective function
profit = sell_price * n_steel_quant - pulp.lpSum(cost[k] * (x[k] / 1000) for k in range(K)) - melt_price * n_steel_quant - mang_price * y
problem += profit, "Total_Profit"

# Constraints
# Total steel production constraint
problem += pulp.lpSum(x[k] for k in range(K)) + y == n_steel_quant, "Total_Steel_Production"

# Manganese content constraint
problem += pulp.lpSum((contmn[k] / 100) * x[k] for k in range(K)) + y >= (mn_percent / 100) * n_steel_quant, "Manganese_Content"

# Silicon content lower bound constraint
problem += pulp.lpSum((contsi[k] / 100) * x[k] for k in range(K)) >= (si_min / 100) * n_steel_quant, "Silicon_Min_Bound"

# Silicon content upper bound constraint
problem += pulp.lpSum((contsi[k] / 100) * x[k] for k in range(K)) <= (si_max / 100) * n_steel_quant, "Silicon_Max_Bound"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')