import pulp

# Input data
data = {'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0,
        'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4],
        'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}

# Define problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Variables for amount of each mineral melted
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("Amount", range(K), lowBound=0)

# Variable for amount of Manganese added
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Objective function
profit = data['sell_price'] * data['n_steel_quant'] - pulp.lpSum(
    (data['cost'][k] * amount[k] * 1000) + (data['melt_price'] * amount[k]) for k in range(K)
) - (data['mang_price'] * num_mang)
problem += profit

# Constraints
# Total quantity of steel produced
problem += pulp.lpSum(amount[k] * data['contsi'][k] for k in range(K)) + (num_mang * 0) >= data['si_min'] * data['n_steel_quant'], "Silicon_Min_Constraint"
problem += pulp.lpSum(amount[k] * data['contsi'][k] for k in range(K)) + (num_mang * 0) <= data['si_max'] * data['n_steel_quant'], "Silicon_Max_Constraint"

# Manganese content constraint
total_manganese = pulp.lpSum(amount[k] * data['contmn'][k] for k in range(K)) + num_mang
problem += total_manganese >= data['mn_percent'] * data['n_steel_quant'], "Manganese_Constraint"

# Solve the problem
problem.solve()

# Output results
result = {
    "amount": [amount[k].varValue for k in range(K)],
    "num_mang": num_mang.varValue
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')