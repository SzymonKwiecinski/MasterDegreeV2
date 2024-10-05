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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
K = len(data['contsi'])
amount_vars = [pulp.LpVariable(f'amount_{k+1}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective Function
revenue = data['sell_price'] * data['n_steel_quant']
costs = sum(data['cost'][k] * amount_vars[k] / 1000 for k in range(K)) \
        + data['melt_price'] * data['n_steel_quant'] \
        + data['mang_price'] * num_mang
profit = revenue - costs
problem += profit

# Constraints
# Constraint 1: Total steel production quantity
problem += (sum(amount_vars) + num_mang == data['n_steel_quant'])

# Constraint 2: Manganese content
problem += (sum(data['contmn'][k] * amount_vars[k] for k in range(K)) + num_mang >= data['mn_percent'] * data['n_steel_quant'])

# Constraint 3: Silicon content min
problem += (sum(data['contsi'][k] * amount_vars[k] for k in range(K)) >= data['si_min'] * data['n_steel_quant'])

# Constraint 4: Silicon content max
problem += (sum(data['contsi'][k] * amount_vars[k] for k in range(K)) <= data['si_max'] * data['n_steel_quant'])

# Solve the problem
problem.solve()

# Prepare the output
amount = [pulp.value(var) for var in amount_vars]
output = {
    "amount": amount,
    "num_mang": [pulp.value(num_mang)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')