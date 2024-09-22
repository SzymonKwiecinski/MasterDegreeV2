import pulp

# Data from the input JSON
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

# Problem definition
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # amounts of minerals
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # amount of manganese added

# Objective function
profit = (data['sell_price'] - pulp.lpSum((data['cost'][k] / 1000 + data['melt_price']) * amount[k] for k in range(K)) - data['mang_price'] * num_mang) * data['n_steel_quant']
problem += profit, "Total_Profit"

# Constraints
# Total steel produced must equal the required steel
problem += (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / 100 + num_mang * (data['mn_percent'] / 100) >= data['n_steel_quant']), "Steel_Production"

# Manganese constraint
problem += (num_mang / data['n_steel_quant'] >= data['mn_percent'] / 100), "Manganese_Constraint"

# Silicon percentage constraints
problem += (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / 100 >= data['si_min'] * data['n_steel_quant']), "Silicon_Min_Constraint"
problem += (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / 100 <= data['si_max'] * data['n_steel_quant']), "Silicon_Max_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')