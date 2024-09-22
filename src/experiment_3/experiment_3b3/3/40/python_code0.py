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

# Parameters 
K = len(data['contsi'])

# Define the problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0, cat='Continuous')

# Objective Function
problem += (data['n_steel_quant'] * data['sell_price'] 
            - sum(data['cost'][k] / 1000 * amount[k] + data['melt_price'] * amount[k] for k in range(K))
            - data['mang_price'] * num_mang)

# Manganese content constraint
problem += (sum(data['contmn'][k] / 100 * amount[k] for k in range(K)) + num_mang 
            >= data['n_steel_quant'] * data['mn_percent'] / 100)

# Silicon content minimum constraint
problem += (sum(data['contsi'][k] / 100 * amount[k] for k in range(K)) 
            >= data['n_steel_quant'] * data['si_min'] / 100)

# Silicon content maximum constraint
problem += (sum(data['contsi'][k] / 100 * amount[k] for k in range(K)) 
            <= data['n_steel_quant'] * data['si_max'] / 100)

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')