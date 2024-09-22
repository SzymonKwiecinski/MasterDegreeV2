import pulp
import json

# Input data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 
        'mang_price': 8.0, 'cost': [21, 25, 15], 
        'sell_price': 0.45, 'melt_price': 0.005}

# Problem parameters
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
K = len(contsi)  # Number of minerals
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Amount of each mineral melted
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of Manganese added

# Objective function: Maximize profit
profit = (sell_price * n_steel_quant) - (melt_price * sum(amount[k] for k in range(K))) - (mang_price * num_mang)
problem += profit

# Constraints
# Manganese content constraint
problem += (sum((contmn[k] / 100) * amount[k] for k in range(K)) + (num_mang) >= mn_percent * n_steel_quant), "Manganese_Constraint"

# Silicon content constraints
problem += (sum((contsi[k] / 100) * amount[k] for k in range(K)) >= si_min * n_steel_quant), "Si_Min_Constraint"
problem += (sum((contsi[k] / 100) * amount[k] for k in range(K)) <= si_max * n_steel_quant), "Si_Max_Constraint"

# Total weight constraint
problem += (sum(amount[k] for k in range(K)) + num_mang == n_steel_quant), "Total_Weight_Constraint"

# Solve the problem
problem.solve()

# Output results
results = {
    "amount": [amount[k].varValue for k in range(K)],
    "num_mang": num_mang.varValue
}
print(json.dumps(results))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')