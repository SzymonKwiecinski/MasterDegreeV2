import pulp

# Data from the given JSON
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

# Unpacking the data
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

# Problem definition
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
amounts = [pulp.LpVariable(f"amount_{k+1}", lowBound=0, cat='Continuous') for k in range(K)]
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

# Objective function: Maximize profit
problem += (
    sell_price * n_steel_quant -
    sum(cost[k] * amounts[k] / 1000 for k in range(K)) -
    melt_price * n_steel_quant -
    mang_price * num_mang
)

# Constraints

# Total weight constraint
problem += (sum(amounts) + num_mang == n_steel_quant)

# Manganese content constraint
problem += (sum(contmn[k] * amounts[k] for k in range(K)) + num_mang >= mn_percent * n_steel_quant)

# Silicon content constraints
problem += (sum(contsi[k] * amounts[k] for k in range(K)) >= si_min * n_steel_quant)
problem += (sum(contsi[k] * amounts[k] for k in range(K)) <= si_max * n_steel_quant)

# Solve the problem
problem.solve()

# Prepare the results
result = {
    "amount": [pulp.value(amounts[k]) for k in range(K)],
    "num_mang": pulp.value(num_mang)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')