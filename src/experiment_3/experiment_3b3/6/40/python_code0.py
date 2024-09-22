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

# Parameters
n = data['n_steel_quant']
mn = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']
K = len(contsi)

# Problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

# Objective Function
profit = (n * sell_price -
          pulp.lpSum([(cost[k] / 1000) * x[k] for k in range(K)]) -
          melt_price * pulp.lpSum(x) -
          mang_price * y)

problem += profit

# Constraints
# 1. Total weight of steel produced
problem += pulp.lpSum([(x[k] * contsi[k] / 100) for k in range(K)]) + y >= n * mn / 100

# 2. Silicon content constraint
problem += pulp.lpSum([(x[k] * contsi[k] / 100) for k in range(K)]) >= si_min
problem += pulp.lpSum([(x[k] * contsi[k] / 100) for k in range(K)]) <= si_max

# 3. Manganese content constraint
problem += pulp.lpSum([(x[k] * contmn[k] / 100) for k in range(K)]) + y >= n * mn / 100

# Solve
problem.solve()

# Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')