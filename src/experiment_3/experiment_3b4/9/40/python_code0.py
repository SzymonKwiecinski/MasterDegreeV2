import pulp

# Data extracted from the provided JSON
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

# Number of types of metal
K = len(data['cost'])

# Initialize the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(K)]
y = pulp.LpVariable('y', lowBound=0)

# Objective function
objective = (data['n_steel_quant'] * data['sell_price']
             - sum((data['cost'][k] + data['melt_price']) * x[k] for k in range(K))
             - data['mang_price'] * y)
problem += objective

# Constraint 1: Total Steel Production Constraint
problem += pulp.lpSum(x[k] for k in range(K)) == data['n_steel_quant'] / 1000

# Constraint 2: Manganese Content Constraint
problem += pulp.lpSum(data['contmn'][k] * x[k] for k in range(K)) + y >= (data['mn_percent'] / 100) * data['n_steel_quant']

# Constraint 3: Silicon Content Constraints
problem += pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) >= (data['si_min'] / 100) * data['n_steel_quant']
problem += pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) <= (data['si_max'] / 100) * data['n_steel_quant']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')