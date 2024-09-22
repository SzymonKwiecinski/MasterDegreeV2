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
K = len(data['contsi'])  # Number of different minerals
amount_k = pulp.LpVariable.dicts("amount_k", range(K), lowBound=0)  # Amount of mineral k
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of manganese

# Objective Function
profit = (data['n_steel_quant'] * data['sell_price'] - 
          pulp.lpSum((data['cost'][k] / 1000) * amount_k[k] for k in range(K)) - 
          data['melt_price'] * pulp.lpSum(amount_k[k] for k in range(K)) - 
          data['mang_price'] * num_mang)

problem += profit, "Profit"

# Constraints
# Manganese constraint
problem += (pulp.lpSum(data['contmn'][k] * amount_k[k] for k in range(K)) + num_mang) >= data['mn_percent'] * data['n_steel_quant'], "Manganese_Constraint"

# Silicon constraints
problem += (pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(K)) / data['n_steel_quant']) >= data['si_min'], "Silicon_Min_Constraint"
problem += (pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(K)) / data['n_steel_quant']) <= data['si_max'], "Silicon_Max_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')