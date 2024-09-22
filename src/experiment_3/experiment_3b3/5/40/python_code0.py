import pulp

# Data provided in JSON format
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
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
K = len(data['contsi'])
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

# Objective function
profit = (
    data['n_steel_quant'] * data['sell_price']
    - pulp.lpSum((data['cost'][k] / 1000 + data['melt_price']) * x[k] for k in range(K))
    - data['mang_price'] * y
)
problem += profit

# Constraints

# 1. Total steel produced must meet quantity requirement for manganese
problem += (
    pulp.lpSum((data['contmn'][k] / 100) * x[k] for k in range(K)) + y 
    >= data['n_steel_quant'] * (data['mn_percent'] / 100)
)

# 2. Silicon content must be within specified limits
problem += (
    data['si_min'] 
    <= pulp.lpSum((data['contsi'][k] / 100) * x[k] for k in range(K))
    <= data['si_max']
)

# 3. Total steel produced must match the steel quantity required
problem += (
    pulp.lpSum(x[k] for k in range(K)) + y 
    == data['n_steel_quant']
)

# Solve the problem
problem.solve()

# Output the results
amount = [pulp.value(x[k]) for k in range(K)]
num_mang = pulp.value(y)
print(f'Amount of each mineral melted: {amount}')
print(f'Amount of Manganese added: {num_mang}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')