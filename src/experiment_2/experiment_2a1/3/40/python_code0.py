import pulp

# Input data
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

# Problem variables
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

# Create the LP problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Variables for the amount of each mineral melted
K = len(contsi)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Variable for the amount of Manganese added
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Objective function: Maximize profit
profit = (sell_price * n_steel_quant) - (sum([(cost[k] + melt_price) * amount[k] / 1000 for k in range(K)]) + (mang_price * num_mang))
problem += profit

# Constraints
# Steel weight must equal the total weight of minerals plus manganese
problem += pulp.lpSum([(amount[k] * contsi[k] / 100) for k in range(K)]) + (num_mang * 1) == n_steel_quant

# Manganese percentage constraint
problem += (pulp.lpSum([(amount[k] * contmn[k] / 100) for k in range(K)]) + num_mang) >= mn_percent * n_steel_quant

# Silicon content constraints
problem += (pulp.lpSum([(amount[k] * contsi[k] / 100) for k in range(K)]) >= si_min * n_steel_quant)
problem += (pulp.lpSum([(amount[k] * contsi[k] / 100) for k in range(K)]) <= si_max * n_steel_quant)

# Solve the problem
problem.solve()

# Prepare output
output = {
    "amount": [amount[k].varValue for k in range(K)],
    "num_mang": num_mang.varValue
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')