import pulp

# Data from JSON format
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

# Define the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(len(data['cost'])), lowBound=0, cat='Continuous')
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')

# Objective Function
profit = data['sell_price'] * data['n_steel_quant'] - \
         pulp.lpSum(x[k] * data['cost'][k] for k in range(len(data['cost']))) - \
         y * data['mang_price'] - \
         (pulp.lpSum(x[k] for k in range(len(data['cost']))) + y / 1000.0) * data['n_steel_quant'] * data['melt_price']
problem += profit, "Total_Profit"

# Constraints
problem += pulp.lpSum(x[k] for k in range(len(data['cost']))) + y / 1000.0 == data['n_steel_quant'], "Total_Steel_Production"
problem += pulp.lpSum(x[k] * data['contmn'][k] for k in range(len(data['cost']))) + (y / data['n_steel_quant']) >= data['mn_percent'], "Manganese_Requirement"
problem += pulp.lpSum(x[k] * data['contsi'][k] for k in range(len(data['cost']))) >= data['si_min'], "Silicon_Lower_Bound"
problem += pulp.lpSum(x[k] * data['contsi'][k] for k in range(len(data['cost']))) <= data['si_max'], "Silicon_Upper_Bound"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')