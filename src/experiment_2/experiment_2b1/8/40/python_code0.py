import pulp
import json

# Input data from the given JSON format
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

# Defining the problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Variables
K = len(contsi)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Amount of each mineral melted
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of Manganese added

# Objective function
profit = (sell_price * n_steel_quant) - (pulp.lpSum([(cost[k] * amount[k])/1000 for k in range(K)]) + (melt_price * pulp.lpSum([amount[k] for k in range(K)])) + (mang_price * num_mang))
problem += profit

# Constraints
# Total weight of steel to be produced
problem += (pulp.lpSum([amount[k] * (contmn[k] / 100) for k in range(K)]) + num_mang) >= n_steel_quant * mn_percent, "MnRequirement")
problem += (pulp.lpSum([amount[k] * (contsi[k] / 100) for k in range(K)]) >= si_min * n_steel_quant, "SiMinRequirement")
problem += (pulp.lpSum([amount[k] * (contsi[k] / 100) for k in range(K)]) <= si_max * n_steel_quant, "SiMaxRequirement")

# Solve the problem
problem.solve()

# Output results
amount_values = [amount[k].varValue for k in range(K)]
num_mang_value = num_mang.varValue

result = {
    "amount": amount_values,
    "num_mang": num_mang_value
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')