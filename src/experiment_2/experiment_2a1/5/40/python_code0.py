import json
import pulp

# Input data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 
        'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}

# Extracting data
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

# Setting up the problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Variables
K = len(cost)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Amount of each mineral melted
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of Manganese added

# Objective Function
profit = (sell_price * n_steel_quant) - (pulp.lpSum([(cost[k]/1000)*amount[k] for k in range(K)]) + 
              (melt_price * pulp.lpSum([amount[k] for k in range(K)])) + 
              (mang_price * num_mang))
problem += profit

# Constraints
# Manganese content constraint
problem += (pulp.lpSum([contmn[k] * amount[k] for k in range(K)]) + num_mang) >= mn_percent * n_steel_quant, "Mn_Constraint"

# Silicon content constraints
problem += (pulp.lpSum([contsi[k] * amount[k] for k in range(K)]) / n_steel_quant) >= si_min, "Si_Min_Constraint"
problem += (pulp.lpSum([contsi[k] * amount[k] for k in range(K)]) / n_steel_quant) <= si_max, "Si_Max_Constraint"

# Total output constraint
problem += pulp.lpSum(amount[k] for k in range(K)) + num_mang == n_steel_quant, "Total_Output_Constraint"

# Solve the problem
problem.solve()

# Prepare the output
amount_solution = [amount[k].varValue for k in range(K)]
num_mang_solution = num_mang.varValue

output = {
    "amount": amount_solution,
    "num_mang": num_mang_solution
}

# Print the results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')