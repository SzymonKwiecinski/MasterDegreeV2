import pulp
import json

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

# Create a linear programming problem
problem = pulp.LpProblem("SteelProduction", pulp.LpMaximize)

# Variables for the amount of each mineral melted
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("Amount", range(K), lowBound=0)

# Variable for the amount of Manganese added
num_mang = pulp.LpVariable("NumMang", lowBound=0)

# Objective function: maximize profit
profit_per_ton = data['sell_price'] - data['melt_price'] - pulp.lpSum(data['cost'][k] * amount[k] / 1000 for k in range(K)) - data['mang_price'] * num_mang
problem += profit_per_ton * data['n_steel_quant'], "Total_Profit"

# Constraints
# Total content must meet the manganese percentage requirement
problem += (pulp.lpSum(data['contmn'][k] * amount[k] for k in range(K)) + num_mang) >= data['mn_percent'] * data['n_steel_quant'], "Mn_Requirement"

# Total content must meet the silicon percentage requirement
silicon_content = pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K))
problem += silicon_content >= data['si_min'] * data['n_steel_quant'], "Si_Min_Requirement"
problem += silicon_content <= data['si_max'] * data['n_steel_quant'], "Si_Max_Requirement"

# Solve the problem
problem.solve()

# Prepare results
result_amount = [amount[k].varValue for k in range(K)]
result_num_mang = num_mang.varValue

# Output results
output = {
    "amount": result_amount,
    "num_mang": result_num_mang
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')