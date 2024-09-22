import pulp

# Data provided in JSON format
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

# Initialize the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision variables
K = len(data['contsi'])
amount_k = pulp.LpVariable.dicts("amount_k", range(K), lowBound=0, cat='Continuous')
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

# Objective function
problem += (
    (data['sell_price'] - data['melt_price']) * data['n_steel_quant'] -
    pulp.lpSum((data['cost'][k] / 1000) * amount_k[k] for k in range(K)) -
    data['mang_price'] * num_mang,
    "Total_Profit"
)

# Constraints
problem += (
    pulp.lpSum(data['contmn'][k] * amount_k[k] for k in range(K)) + num_mang >= 
    (data['mn_percent'] / 100) * data['n_steel_quant'],
    "Mn_Requirement"
)

problem += (
    (data['si_min'] * data['n_steel_quant'] <= 
     pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(K)) + num_mang) &
     (pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(K)) + num_mang <= 
     data['si_max'] * data['n_steel_quant']),
    "Si_Requirement"
)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')