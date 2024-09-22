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

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(3)]
y = pulp.LpVariable('y', lowBound=0)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
problem += (
    data['n_steel_quant'] * data['sell_price'] - (
        pulp.lpSum(data['cost'][k] * x[k] for k in range(3)) +
        (pulp.lpSum(x) + y) * data['melt_price'] +
        y * data['mang_price']
    )
)

# Constraints
problem += pulp.lpSum(x) + y == data['n_steel_quant'], "Total_Steel_Production"

problem += (
    (pulp.lpSum(data['contmn'][k] * x[k] for k in range(3)) + y) /
    (pulp.lpSum(x) + y) >= data['mn_percent'] / 100
), "Manganese_Content"

problem += (
    (pulp.lpSum(data['contsi'][k] * x[k] for k in range(3))) /
    (pulp.lpSum(x) + y) >= data['si_min'] / 100
), "Silicon_Content_Min"

problem += (
    (pulp.lpSum(data['contsi'][k] * x[k] for k in range(3))) /
    (pulp.lpSum(x) + y) <= data['si_max'] / 100
), "Silicon_Content_Max"

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')