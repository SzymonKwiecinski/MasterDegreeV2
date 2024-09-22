import pulp

# Data from the JSON
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

# Problem Initialization
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
K = len(data['contsi'])
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective Function
profit = (
    data['n_steel_quant'] * data['sell_price']
    - sum((amount[k] * data['melt_price'] + (data['cost'][k] / 1000) * amount[k]) for k in range(K))
    - num_mang * data['mang_price']
)
problem += profit

# Constraints

# Total weight of steel produced
problem += (
    sum(amount[k] * (data['contsi'][k] / 100) for k in range(K)) + num_mang * (data['contmn'][0] / 100)
    == data['n_steel_quant']
)

# Percentage of Manganese
problem += (
    num_mang * (data['contmn'][0] / 100) / data['n_steel_quant']
    >= data['mn_percent'] / 100
)

# Percentage of Silicon
problem += (
    sum(amount[k] * (data['contsi'][k] / 100) for k in range(K))
    >= data['si_min']
)
problem += (
    sum(amount[k] * (data['contsi'][k] / 100) for k in range(K))
    <= data['si_max']
)

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')