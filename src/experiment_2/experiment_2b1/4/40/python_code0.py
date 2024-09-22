import pulp

# Input data
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

# Setting up the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Objective function: Maximize profit
revenue = data['n_steel_quant'] * data['sell_price']
costs = pulp.lpSum((data['cost'][k] * amount[k] / 1000) + (data['melt_price'] * amount[k]) for k in range(K)) + (data['mang_price'] * num_mang)
profit = revenue - costs
problem += profit

# Constraints
# Total weight of steel produced must be n_steel_quant
problem += pulp.lpSum((amount[k] * (data['contsi'][k] / 100)) for k in range(K)) + num_mang >= data['n_steel_quant'] * (data['mn_percent'] / 100), "Mn_Requirement"
problem += pulp.lpSum((amount[k] * (data['contsi'][k] / 100)) for k in range(K)) >= data['n_steel_quant'] * (data['si_min'] / 100), "Si_Min_Requirement"
problem += pulp.lpSum((amount[k] * (data['contsi'][k] / 100)) for k in range(K)) <= data['n_steel_quant'] * (data['si_max'] / 100), "Si_Max_Requirement"

# Solve the problem
problem.solve()

# Output the results
amount_solution = [amount[k].varValue for k in range(K)]
num_mang_solution = num_mang.varValue

output = {
    "amount": amount_solution,
    "num_mang": num_mang_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')