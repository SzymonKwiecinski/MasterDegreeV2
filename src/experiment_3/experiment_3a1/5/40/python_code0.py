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

# Create the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Objective function
profit = (data['sell_price'] * data['n_steel_quant'] - 
          (pulp.lpSum((data['cost'][k] / 1000) * amount[k] for k in range(K)) + 
          data['melt_price'] * pulp.lpSum(amount[k] for k in range(K)) + 
          data['mang_price'] * num_mang))

problem += profit

# Constraints
# Manganese requirement
problem += (pulp.lpSum(data['contmn'][k] * amount[k] for k in range(K)) + num_mang >= 
             (data['mn_percent'] / 100) * data['n_steel_quant'])

# Silicon content limits
problem += (data['si_min'] <= (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / data['n_steel_quant']))
problem += (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / data['n_steel_quant'] <= data['si_max'])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')