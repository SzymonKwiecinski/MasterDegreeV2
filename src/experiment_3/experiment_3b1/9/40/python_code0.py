import pulp

# Data from the JSON format
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
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']

# Number of minerals
K = len(contsi)

# Create the problem variable
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0, cat='Continuous')
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

# Objective function
profit = n_steel_quant * sell_price - pulp.lpSum((cost[k] / 1000) * amount[k] + melt_price * amount[k] for k in range(K)) - mang_price * num_mang
problem += profit, "Total_Profit"

# Constraints
# Steel production requirement
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) >= n_steel_quant * (si_min / 100), "Steel_Production_Min"
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= n_steel_quant * (si_max / 100), "Steel_Production_Max"

# Manganese requirement
problem += pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang >= n_steel_quant * (mn_percent / 100), "Manganese_Requirement"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')