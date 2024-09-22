import pulp

# Data provided
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

# Create problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(len(data['contsi']))]
n_mang = pulp.LpVariable('n_mang', lowBound=0)

# Objective function
profit = data['sell_price'] * data['n_steel_quant'] \
          - sum((data['cost'][k] / 1000 + data['melt_price']) * x[k] for k in range(len(x))) \
          - data['mang_price'] * n_mang

problem += profit

# Constraints
# 1. Total weight of steel produced
problem += n_mang + sum(x) == data['n_steel_quant']

# 2. Manganese percentage in steel
problem += (sum(data['contmn'][k] * x[k] for k in range(len(x))) + n_mang) >= (data['mn_percent'] / 100) * data['n_steel_quant']

# 3. Silicon percentage in steel
problem += sum(data['contsi'][k] * x[k] for k in range(len(x))) >= data['si_min'] * data['n_steel_quant']
problem += sum(data['contsi'][k] * x[k] for k in range(len(x))) <= data['si_max'] * data['n_steel_quant']

# Solve the problem
problem.solve()

# Output results
amount = [pulp.value(x[k]) for k in range(len(x))]
num_mang = pulp.value(n_mang)

print("Amounts of each mineral melted:", amount)
print("Amount of Manganese directly added:", num_mang)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')