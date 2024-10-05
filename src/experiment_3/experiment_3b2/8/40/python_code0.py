import pulp

# Given data
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

# Define the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
K = len(data['contsi'])
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Amount of mineral k used (in thousand tons)
y = pulp.LpVariable("y", lowBound=0)  # Amount of manganese directly added (in tons)

# Objective Function
profit = data['n_steel_quant'] * data['sell_price'] - \
         pulp.lpSum(x[k] * data['cost'][k] + x[k] * 1000 * data['melt_price'] for k in range(K)) - \
         y * data['mang_price']

problem += profit

# Constraints
# Total steel production requirement
problem += pulp.lpSum(x[k] * 1000 for k in range(K)) + y == data['n_steel_quant'], "Total_Production_Requirement"

# Manganese percentage constraint
problem += (pulp.lpSum(x[k] * 1000 * data['contmn'][k] for k in range(K)) + y) / data['n_steel_quant'] >= data['mn_percent'], "Manganese_Percentage_Constraint"

# Minimum Silicon constraint
problem += pulp.lpSum(x[k] * 1000 * data['contsi'][k] for k in range(K)) >= data['si_min'] * data['n_steel_quant'], "Min_Silicon_Constraint"

# Maximum Silicon constraint
problem += pulp.lpSum(x[k] * 1000 * data['contsi'][k] for k in range(K)) <= data['si_max'] * data['n_steel_quant'], "Max_Silicon_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')