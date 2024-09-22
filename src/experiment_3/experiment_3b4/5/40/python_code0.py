import pulp

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

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

K = len(data['contsi'])

# Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function
problem += (
    data['sell_price'] * data['n_steel_quant'] 
    - sum((data['cost'][k] / 1000) * amount[k] for k in range(K))
    - data['mang_price'] * num_mang
    - data['melt_price'] * sum(amount[k] for k in range(K))
), "Objective"

# Constraints
problem += (
    sum(data['contmn'][k] * amount[k] for k in range(K)) + num_mang 
    == data['mn_percent'] * data['n_steel_quant']
), "Manganese Requirement"

problem += (
    sum(data['contsi'][k] * amount[k] for k in range(K)) 
    >= data['si_min'] * data['n_steel_quant']
), "Silicon Lower Bound Requirement"

problem += (
    sum(data['contsi'][k] * amount[k] for k in range(K)) 
    <= data['si_max'] * data['n_steel_quant']
), "Silicon Upper Bound Requirement"

problem += (
    sum(amount[k] for k in range(K)) 
    == data['n_steel_quant']
), "Total Mass of Minerals"

# Solve the problem
problem.solve()

# Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')