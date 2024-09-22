import pulp

# Data extracted from JSON format
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

# Decision Variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # amount_k for each mineral
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # num_mang

# Objective Function
profit = (
    data['sell_price'] * data['n_steel_quant'] -
    pulp.lpSum((data['cost'][k] * (amount[k] / 1000) + data['melt_price'] * amount[k]) for k in range(K)) -
    data['mang_price'] * num_mang
)

problem += profit, "Total_Profit"

# Constraints
# Total steel production (from Si)
problem += (
    pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) == data['n_steel_quant'] * (data['si_min'] / 100), 
    "Total_Si_Production"
)

# Minimum percentage of Manganese
problem += (
    pulp.lpSum(data['contmn'][k] * amount[k] for k in range(K)) + num_mang >= data['n_steel_quant'] * (data['mn_percent'] / 100), 
    "Min_Manganese"
)

# Silicon percentage constraints
problem += (
    data['n_steel_quant'] * (data['si_min'] / 100) <= pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) <= 
    data['n_steel_quant'] * (data['si_max'] / 100), 
    "Si_Percentage_Constraints"
)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')