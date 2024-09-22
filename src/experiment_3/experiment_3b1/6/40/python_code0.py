import pulp

# Data from the provided JSON format
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

# Extracting values from the data for convenience
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

# Create the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # amount_k
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # num_mang

# Objective function
profit = n_steel_quant * sell_price - pulp.lpSum((cost[k] / 1000) * amount[k] + melt_price * amount[k] for k in range(K)) - mang_price * num_mang
problem += profit, "Total_Profit"

# Constraints
# Manganese content constraint
problem += pulp.lpSum((amount[k] * contmn[k] / 100) for k in range(K)) + num_mang >= (mn_percent / 100) * n_steel_quant, "Manganese_Content"

# Silicon content constraints
problem += (pulp.lpSum((amount[k] * contsi[k] / 100) for k in range(K)) / n_steel_quant) >= si_min, "Silicon_Min_Content"
problem += (pulp.lpSum((amount[k] * contsi[k] / 100) for k in range(K)) / n_steel_quant) <= si_max, "Silicon_Max_Content"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')