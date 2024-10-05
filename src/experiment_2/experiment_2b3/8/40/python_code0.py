import pulp

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Extract data from the input
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

K = len(contsi)

# Define decision variables
amount = [pulp.LpVariable(f"amount_{k}", lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Objective function
profit = (sell_price - melt_price) * n_steel_quant
profit -= sum((cost[k] / 1000.0) * amount[k] for k in range(K))
profit -= mang_price * num_mang
problem += profit

# Constraints
# Total weight of minerals and manganese must equal the steel quantity
problem += sum(amount[k] for k in range(K)) + num_mang == n_steel_quant

# Constraint on manganese content
problem += sum(contmn[k] * amount[k] for k in range(K)) + num_mang >= mn_percent * n_steel_quant

# Constraint on silicon content
problem += sum(contsi[k] * amount[k] for k in range(K)) >= si_min * n_steel_quant
problem += sum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant

# Solve the problem
problem.solve()

# Prepare output
output = {
    "amount": [pulp.value(amount[k]) for k in range(K)],
    "num_mang": pulp.value(num_mang)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')