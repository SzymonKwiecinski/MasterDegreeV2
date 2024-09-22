import pulp

# Define the data
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

# Number of minerals
K = len(data['cost'])

# Define the problem
problem = pulp.LpProblem("Maximize_Profit_Steel_Production", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

# Objective function
profit = (data['n_steel_quant'] * data['sell_price'] - 
          pulp.lpSum([x[k] * (data['cost'][k] + data['melt_price']) for k in range(K)]) -
          y * data['mang_price'])

problem += profit

# Constraints
# Steel Quantity Constraint
problem += (pulp.lpSum([x[k] * 1000 for k in range(K)]) + y == data['n_steel_quant'])

# Manganese Content Constraint
problem += (pulp.lpSum([x[k] * 1000 * (data['contmn'][k] / 100) for k in range(K)]) + y >= 
            data['n_steel_quant'] * (data['mn_percent'] / 100))

# Silicon Content Constraints
problem += (pulp.lpSum([x[k] * 1000 * (data['contsi'][k] / 100) for k in range(K)]) >= 
            data['n_steel_quant'] * (data['si_min'] / 100))

problem += (pulp.lpSum([x[k] * 1000 * (data['contsi'][k] / 100) for k in range(K)]) <= 
            data['n_steel_quant'] * (data['si_max'] / 100))

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')