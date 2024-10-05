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

# Decision Variables
x = pulp.LpVariable.dicts('x', range(len(data['cost'])), lowBound=0, cat='Continuous')
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

# Objective Function
problem += (
    data['sell_price'] * data['n_steel_quant'] 
    - (
        sum(data['cost'][k] * x[k] for k in range(len(data['cost']))) 
        + data['mang_price'] * y 
        + data['melt_price'] * data['n_steel_quant']
    )
)

# Constraints
# Total quantity constraint
problem += (
    sum(x[k] for k in range(len(data['cost']))) + y == data['n_steel_quant']
)

# Manganese content constraint
problem += (
    sum(data['contmn'][k] * x[k] for k in range(len(data['contmn']))) + y >= data['mn_percent'] * data['n_steel_quant']
)

# Silicon content constraints
problem += (
    data['si_min'] * data['n_steel_quant'] <= sum(data['contsi'][k] * x[k] for k in range(len(data['contsi'])))
)
problem += (
    sum(data['contsi'][k] * x[k] for k in range(len(data['contsi']))) <= data['si_max'] * data['n_steel_quant']
)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')