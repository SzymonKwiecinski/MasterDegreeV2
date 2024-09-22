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

# Number of types of alloys
K = len(data['contsi'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f"x{k}", lowBound=0) for k in range(K)]
y = pulp.LpVariable("y", lowBound=0)

# Objective function
profit = (
    data['sell_price'] * data['n_steel_quant']
    - pulp.lpSum([data['cost'][k] * x[k] for k in range(K)])
    - y * data['mang_price']
    - pulp.lpSum([data['melt_price'] * x[k] for k in range(K)])
)
problem += profit

# Constraints

# 1. Total amount of steel
problem += (pulp.lpSum([1000 * x[k] for k in range(K)]) + y == data['n_steel_quant'])

# 2. Manganese content
problem += (pulp.lpSum([1000 * x[k] * data['contmn'][k] for k in range(K)]) + y >= data['n_steel_quant'] * data['mn_percent'])

# 3. Silicon content
problem += (data['si_min'] * data['n_steel_quant'] <= pulp.lpSum([1000 * x[k] * data['contsi'][k] for k in range(K)]) <= data['si_max'] * data['n_steel_quant'])

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')