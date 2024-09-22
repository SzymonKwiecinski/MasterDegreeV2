import pulp

# Given data
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

# Create a LP maximization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function
profit = (
    sell_price * n_steel_quant -
    pulp.lpSum(amount[k] * (cost[k]/1000 + melt_price) for k in range(K)) -
    num_mang * mang_price
)
problem += profit, "Total Profit"

# Constraints
# Total steel quantity constraint (sum of minerals and manganese)
problem += pulp.lpSum(amount) + num_mang == n_steel_quant, "Total Steel"

# Manganese percentage constraint
problem += (
    pulp.lpSum(amount[k] * contmn[k] for k in range(K)) + num_mang >= mn_percent * n_steel_quant,
    "Manganese Requirement"
)

# Silicon percentage range constraint
problem += (
    pulp.lpSum(amount[k] * contsi[k] for k in range(K)) >= si_min * n_steel_quant,
    "Silicon Minimum Requirement"
)
problem += (
    pulp.lpSum(amount[k] * contsi[k] for k in range(K)) <= si_max * n_steel_quant,
    "Silicon Maximum Requirement"
)

# Solve the problem
problem.solve()

# Extracting results
amount_values = [pulp.value(amount[k]) for k in range(K)]
num_mang_value = pulp.value(num_mang)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output
output = {
    "amount": amount_values,
    "num_mang": [num_mang_value]
}
output