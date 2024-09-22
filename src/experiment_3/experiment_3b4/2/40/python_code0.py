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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
K = len(data['cost'])
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(K)]  # Non-negative
y = pulp.LpVariable('y', lowBound=0)  # Non-negative

# Objective function
problem += (
    data['sell_price'] * data['n_steel_quant'] 
    - pulp.lpSum(data['cost'][k] * x[k] for k in range(K)) 
    - data['mang_price'] * y 
    - data['melt_price'] * pulp.lpSum(x[k] for k in range(K))
), "Profit"

# Constraints
# Total steel quantity constraint
problem += pulp.lpSum(x[k] for k in range(K)) + y == data['n_steel_quant'], "Total_steel_quantity"

# Manganese content constraint
problem += (
    pulp.lpSum(data['contmn'][k] * x[k] for k in range(K)) + y 
    >= (data['mn_percent'] / 100) * data['n_steel_quant']
), "Manganese_content"

# Silicon content constraints
problem += (
    pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) 
    >= (data['si_min'] / 100) * data['n_steel_quant']
), "Silicon_min_content"

problem += (
    pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) 
    <= (data['si_max'] / 100) * data['n_steel_quant']
), "Silicon_max_content"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')