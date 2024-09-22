import pulp

# Data from json
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

# Unpack data
n_steel_quant = data['n_steel_quant']
mn_percent = data['mn_percent'] / 100
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']

# Number of minerals
K = len(contsi)

# Problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')

# Objective Function
problem += (
    n_steel_quant * sell_price -
    pulp.lpSum([(cost[k] / 1000) * x[k] for k in range(K)]) -
    melt_price * pulp.lpSum(x) -
    mang_price * y
)

# Constraints
# Manganese content
problem += (
    pulp.lpSum([x[k] * contmn[k] for k in range(K)]) >= n_steel_quant * mn_percent
)

# Silicon content
problem += (
    pulp.lpSum([x[k] * contsi[k] for k in range(K)]) >= n_steel_quant * si_min
)
problem += (
    pulp.lpSum([x[k] * contsi[k] for k in range(K)]) <= n_steel_quant * si_max
)

# Total Production Requirement
problem += (
    pulp.lpSum(x) + y == n_steel_quant
)

# Solve
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')