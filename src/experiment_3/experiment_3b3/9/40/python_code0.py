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

# Number of different minerals
num_minerals = len(data['contsi'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(num_minerals)]
num_mang = pulp.LpVariable('num_mang', lowBound=0, cat='Continuous')

# Objective Function
revenue = data['sell_price'] * data['n_steel_quant']
cost_minerals = pulp.lpSum((data['cost'][k] / 1000) * amount[k] for k in range(num_minerals))
cost_melting = data['melt_price'] * pulp.lpSum(amount[k] for k in range(num_minerals))
cost_manganese = data['mang_price'] * num_mang
total_cost = cost_minerals + cost_melting + cost_manganese
problem += revenue - total_cost, "Profit"

# Constraints
# Steel production constraint
problem += pulp.lpSum(amount[k] for k in range(num_minerals)) + num_mang == data['n_steel_quant'], "Steel_Production"

# Manganese percentage constraint
problem += (pulp.lpSum(data['contmn'][k] * amount[k] for k in range(num_minerals)) + num_mang) / data['n_steel_quant'] >= data['mn_percent'] / 100, "Mn_Percentage"

# Silicon percentage constraints
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(num_minerals)) / data['n_steel_quant'] >= data['si_min'], "Si_Min_Constraint"
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(num_minerals)) / data['n_steel_quant'] <= data['si_max'], "Si_Max_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')