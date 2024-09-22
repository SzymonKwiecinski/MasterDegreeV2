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

# Variables
K = len(data['contsi'])
amounts = pulp.LpVariable.dicts("amount", range(K), lowBound=0)
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Objective Function
profit = data['sell_price'] * data['n_steel_quant'] - \
         pulp.lpSum(data['cost'][k] * (amounts[k] / 1000) + data['melt_price'] * amounts[k] for k in range(K)) - \
         data['mang_price'] * num_mang

problem += profit

# Constraints
# Total steel requirement
problem += pulp.lpSum(amounts[k] for k in range(K)) + num_mang == data['n_steel_quant']

# Manganese content requirement
problem += (pulp.lpSum(data['contmn'][k] * amounts[k] for k in range(K)) + num_mang) / data['n_steel_quant'] >= data['mn_percent'] / 100

# Silicon content constraints
problem += (pulp.lpSum(data['contsi'][k] * amounts[k] for k in range(K))) / data['n_steel_quant'] >= data['si_min'] / 100
problem += (pulp.lpSum(data['contsi'][k] * amounts[k] for k in range(K))) / data['n_steel_quant'] <= data['si_max'] / 100

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')