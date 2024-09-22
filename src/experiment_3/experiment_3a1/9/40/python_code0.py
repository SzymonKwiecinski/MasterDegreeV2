import pulp
import json

# Data from the provided JSON
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

# Parameters
n_steel_quant = data['n_steel_quant']
mn_percent = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']
cont_si = data['contsi']
cont_mn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']
K = len(cont_si)

# Problem Definition
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # amount of mineral k melted
m = pulp.LpVariable("m", lowBound=0)  # amount of manganese added

# Objective Function
profit = n_steel_quant * sell_price - pulp.lpSum((cost[k]/1000 * x[k] + melt_price * x[k]) for k in range(K)) - mang_price * m
problem += profit

# Constraints
# 1. Total weight of steel produced
problem += pulp.lpSum((cont_si[k]/100 * x[k]) for k in range(K)) + m == n_steel_quant

# 2. Minimum manganese content
problem += m >= n_steel_quant * (mn_percent / 100)

# 3. Silicon content constraints
problem += pulp.lpSum((cont_si[k]/100 * x[k]) for k in range(K)) >= si_min * n_steel_quant
problem += pulp.lpSum((cont_si[k]/100 * x[k]) for k in range(K)) <= si_max * n_steel_quant

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')