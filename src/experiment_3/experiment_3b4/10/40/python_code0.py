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

K = len(data['contsi'])  # Number of different minerals available

# Variables
amount = [pulp.LpVariable(f"amount_{k}", lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function: Maximize profit
profit = (data['sell_price'] * data['n_steel_quant'] 
          - sum(amount[k] * (data['cost'][k]/1000 + data['melt_price']) for k in range(K))
          - num_mang * data['mang_price'])

problem += profit, "Profit"

# Constraints

# Balance constraint for total steel quantity
problem += sum(amount) + num_mang == data['n_steel_quant'], "Total_Steel_Quantity"

# Manganese content requirement
problem += sum(data['contmn'][k] * amount[k] for k in range(K)) + num_mang >= data['mn_percent'] * data['n_steel_quant'], "Mn_Content"

# Silicon content requirement
problem += data['si_min'] * data['n_steel_quant'] <= sum(data['contsi'][k] * amount[k] for k in range(K)), "Si_Content_Min"
problem += sum(data['contsi'][k] * amount[k] for k in range(K)) <= data['si_max'] * data['n_steel_quant'], "Si_Content_Max"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')