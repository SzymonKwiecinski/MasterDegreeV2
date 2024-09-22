import pulp

# Given data
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

# Set up the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Variables
K = len(data['cost'])
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Amount of mineral k melted
y = pulp.LpVariable("y", lowBound=0)  # Amount of manganese added

# Objective Function
profit = data['n_steel_quant'] * data['sell_price'] - \
         pulp.lpSum(x[k] * data['cost'][k] * 1000 for k in range(K)) - \
         y * data['mang_price'] - \
         pulp.lpSum(x[k] * data['melt_price'] for k in range(K))

problem += profit, "Total_Profit"

# Constraints
# 1. Total weight of steel produced must equal the order quantity
problem += pulp.lpSum(x[k] for k in range(K)) + y == data['n_steel_quant'], "Steel_Weight_Constraint"

# 2. Manganese content constraint
problem += pulp.lpSum(x[k] * data['contmn'][k] for k in range(K)) + 100 * y >= data['n_steel_quant'] * data['mn_percent'], "Manganese_Content_Constraint"

# 3. Silicon content constraints
problem += pulp.lpSum(x[k] * data['contsi'][k] for k in range(K)) >= data['n_steel_quant'] * data['si_min'], "Silicon_Min_Constraint"
problem += pulp.lpSum(x[k] * data['contsi'][k] for k in range(K)) <= data['n_steel_quant'] * data['si_max'], "Silicon_Max_Constraint"

# Solve the problem
problem.solve()

# Output the results
amount = [pulp.value(x[k]) for k in range(K)]
num_mang = pulp.value(y)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Amount of minerals melted: {amount}')
print(f'Amount of manganese added: {num_mang}')