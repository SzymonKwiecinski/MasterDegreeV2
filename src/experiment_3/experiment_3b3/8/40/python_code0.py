import pulp

# Data
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

# Constants
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
K = len(contsi)  # Number of different minerals

# Problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f"amount_{k}", lowBound=0, cat='Continuous') for k in range(K)]
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

# Objective Function
profit = (sell_price - (
    mang_price * num_mang + 
    pulp.lpSum((cost[k] + melt_price) * amount[k] for k in range(K))
)) * n_steel_quant

problem += profit, "Maximize Profit"

# Constraints

# Si Content Constraints
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) >= si_min * n_steel_quant
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant

# Mn Content Constraint
problem += pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang >= mn_percent * n_steel_quant

# Solve
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')