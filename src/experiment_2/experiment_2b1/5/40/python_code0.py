import pulp
import json

# Input data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 
        'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 
        'melt_price': 0.005}

# Define parameters
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

K = len(contsi)

# Create a linear programming problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  # Amount of each mineral melted
num_mang = pulp.LpVariable("num_mang", lowBound=0)  # Amount of Manganese added

# Objective function: maximize profit
profit = (sell_price * n_steel_quant) - (melt_price * sum(amount[k] for k in range(K)) + 
                                           mang_price * num_mang + 
                                           sum(cost[k] * amount[k] / 1000 for k in range(K)))
problem += profit

# Constraints
# Total weight of the produced steel
problem += (sum(contmn[k] * amount[k] for k in range(K)) + num_mang) / n_steel_quant >= mn_percent

# Silicon content constraint
problem += (sum(contsi[k] * amount[k] for k in range(K))) / n_steel_quant >= si_min
problem += (sum(contsi[k] * amount[k] for k in range(K))) / n_steel_quant <= si_max

# Solve the problem
problem.solve()

# Output results
amount_results = [amount[k].varValue for k in range(K)]
num_mang_result = num_mang.varValue

result = {
    "amount": amount_results,
    "num_mang": num_mang_result
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')