import pulp

# Parameters
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

# Initialize the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(len(data['contsi']))]
y = pulp.LpVariable('y', lowBound=0)

# Objective Function
profit = (data['n_steel_quant'] * data['sell_price'] - 
          sum(((data['cost'][k] / 1000) + data['melt_price']) * x[k] for k in range(len(x))) - 
          data['mang_price'] * y)

problem += profit

# Constraints
# Total steel production (Silicon lower bound)
problem += (sum(x[k] * (data['contsi'][k] / 100) for k in range(len(x))) + y 
            >= data['n_steel_quant'] * (data['si_min'] / 100))

# Silicon content within bounds (Silicon upper bound)
problem += (sum(x[k] * (data['contsi'][k] / 100) for k in range(len(x))) + y 
            <= data['n_steel_quant'] * (data['si_max'] / 100))

# Manganese content
problem += (sum(x[k] * (data['contmn'][k] / 100) for k in range(len(x))) + y 
            >= data['n_steel_quant'] * (data['mn_percent'] / 100))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')