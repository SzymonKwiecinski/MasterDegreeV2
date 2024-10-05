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

# Problem
problem = pulp.LpProblem("Steel_Manufacturing", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(len(data['contsi']))]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective Function
profit = (data['sell_price'] * data['n_steel_quant']) - (
    sum((data['cost'][k] / 1000 * amount[k] + data['melt_price'] * amount[k]) for k in range(len(data['contsi'])))
    + data['mang_price'] * num_mang
)
problem += profit

# Constraints
# Mn requirement
problem += sum(data['contmn'][k] * amount[k] for k in range(len(data['contsi']))) + (num_mang / data['n_steel_quant']) >= data['mn_percent'] * data['n_steel_quant']

# Si requirement
problem += sum(data['contsi'][k] * amount[k] for k in range(len(data['contsi']))) >= data['si_min']
problem += sum(data['contsi'][k] * amount[k] for k in range(len(data['contsi']))) <= data['si_max']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')