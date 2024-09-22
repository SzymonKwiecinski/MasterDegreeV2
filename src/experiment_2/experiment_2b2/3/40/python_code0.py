import pulp

# Input Data
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
K = len(contsi)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k+1}', lowBound=0, cat='Continuous') for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0, cat='Continuous')

# Objective Function
profit = (sell_price * n_steel_quant 
          - sum((cost[k]/1000 + melt_price) * amount[k] for k in range(K)) 
          - mang_price * num_mang)
problem += profit

# Constraints
# Total steel quantity constraint
problem += sum(amount) == n_steel_quant

# Manganese percentage constraint
problem += (sum(contmn[k] * amount[k] for k in range(K)) + num_mang) >= mn_percent * n_steel_quant

# Silicon percentage constraints
problem += sum(contsi[k] * amount[k] for k in range(K)) >= si_min * n_steel_quant
problem += sum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant

# Solve the problem
problem.solve()

# Output the results
solution = {
    "amount": [pulp.value(amount[k]) for k in range(K)],
    "num_mang": pulp.value(num_mang)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')