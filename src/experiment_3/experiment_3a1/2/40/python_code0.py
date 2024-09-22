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

# Define the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Define variables
K = len(data['contsi'])
amount_k = pulp.LpVariable.dicts("amount_k", range(K), lowBound=0)
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Objective function
profit = data['n_steel_quant'] * data['sell_price'] - \
         pulp.lpSum((data['cost'][k] / 1000) * amount_k[k] + data['melt_price'] * amount_k[k] for k in range(K)) - \
         data['mang_price'] * num_mang

problem += profit

# Total amount of steel produced
amount_total = pulp.lpSum(amount_k[k] for k in range(K)) + num_mang

# Constraints
problem += (amount_total == data['n_steel_quant'], "Steel_Production_Requirement")

# Manganese content requirement
manganese_content = pulp.lpSum(amount_k[k] * data['contmn'][k] for k in range(K))
problem += (manganese_content >= (data['mn_percent'] / 100) * amount_total, "Manganese_Content_Requirement")

# Silicon content constraints
silicon_content = pulp.lpSum(amount_k[k] * data['contsi'][k] for k in range(K))
problem += (silicon_content >= (data['si_min'] / 100) * amount_total, "Silicon_Content_Min")
problem += (silicon_content <= (data['si_max'] / 100) * amount_total, "Silicon_Content_Max")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')