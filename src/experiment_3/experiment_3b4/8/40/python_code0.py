import pulp

# Data from JSON
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k+1}', lowBound=0) for k in range(len(data['contsi']))]
y = pulp.LpVariable('y', lowBound=0)

# Objective function
revenue = data['sell_price'] * data['n_steel_quant']
costs = sum((data['cost'][k] / 1000) * x[k] for k in range(len(x))) + data['mang_price'] * y + data['melt_price'] * sum(x)
profit = revenue - costs
problem += profit

# Constraints
# Total quantity constraint
problem += sum(x) + y == data['n_steel_quant'], "Total_Quantity"

# Manganese percentage requirement
problem += (sum(data['contmn'][k] * x[k] for k in range(len(x))) + y) / data['n_steel_quant'] >= data['mn_percent'] / 100, "Mn_Percentage"

# Silicon content constraints
problem += sum(data['contsi'][k] * x[k] for k in range(len(x))) / sum(x) >= data['si_min'], "Si_Min"
problem += sum(data['contsi'][k] * x[k] for k in range(len(x))) / sum(x) <= data['si_max'], "Si_Max"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')