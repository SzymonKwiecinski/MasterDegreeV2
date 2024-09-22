import pulp

# Data from the provided JSON format
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

# Create the linear programming problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision Variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # amount_k
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # num_mang

# Objective Function
profit = (data['sell_price'] - (1/1000) * pulp.lpSum(data['cost'][k] * amount[k] for k in range(K)) - \
          data['mang_price'] * num_mang - \
          data['melt_price'] * pulp.lpSum(amount[k] for k in range(K))) * data['n_steel_quant']

problem += profit

# Constraints

# 1. Ensure the required weight of steel
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) + num_mang >= data['mn_percent'] * data['n_steel_quant']

# 2. Ensure Silicon content is within bounds
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) >= data['si_min'] * data['n_steel_quant']
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) <= data['si_max'] * data['n_steel_quant']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')