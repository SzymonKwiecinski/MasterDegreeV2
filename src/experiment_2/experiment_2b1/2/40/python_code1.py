import pulp
import json

# Input data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 
        'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 
        'contmn': [0.45, 0.5, 0.4], 
        'mang_price': 8.0, 
        'cost': [21, 25, 15], 
        'sell_price': 0.45, 
        'melt_price': 0.005}

# Extracting values from input data
n_steel_quant = data['n_steel_quant']
mn_percent = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']

# Define the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Define variables
K = len(contsi)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Amount of each mineral
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of Manganese added

# Objective function
profit = (sell_price * n_steel_quant) - (pulp.lpSum((cost[k] / 1000) * amount[k] + melt_price * amount[k] for k in range(K))) - (mang_price * num_mang)
problem += profit

# Constraints
# Total weight of steel produced must be equal to n_steel_quant
problem += pulp.lpSum((amount[k] * contsi[k] for k in range(K))) + (num_mang * 100) == n_steel_quant * 100

# Manganese percentage constraint
problem += (num_mang / (n_steel_quant * 100)) >= mn_percent

# Silicon percentage constraints
total_si = pulp.lpSum((amount[k] * contsi[k] for k in range(K)))
problem += (total_si / (n_steel_quant * 100)) >= si_min
problem += (total_si / (n_steel_quant * 100)) <= si_max

# Solve the problem
problem.solve()

# Output the results
result = {
    "amount": [amount[k].varValue for k in range(K)],
    "num_mang": num_mang.varValue
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')