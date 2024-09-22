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

# Extracting variables
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

# Create LP problem
problem = pulp.LpProblem("Steel_Manufacture_Profit_Maximization", pulp.LpMaximize)

# Decision variables for the amount of each mineral melted (in tons)
amount = [pulp.LpVariable(f"amount_{k}", lowBound=0) for k in range(K)]

# Decision variable for the amount of manganese directly added (in tons)
num_mang = pulp.LpVariable("num_mang", lowBound=0)

# Objective function
revenue = sell_price * n_steel_quant
cost_minerals = pulp.lpSum([cost[k] / 1000 * amount[k] for k in range(K)])
cost_manganese = mang_price * num_mang
smelting_cost = melt_price * n_steel_quant
total_cost = cost_minerals + cost_manganese + smelting_cost
profit = revenue - total_cost

problem += profit

# Constraints

# 1. Total steel produced must equal the order quantity
problem += pulp.lpSum(amount) + num_mang == n_steel_quant, "Total_Steel"

# 2. Manganese content constraint
problem += pulp.lpSum([contmn[k] * amount[k] for k in range(K)]) + num_mang >= mn_percent * n_steel_quant, "Mn_Content"

# 3. Silicon content constraints
problem += pulp.lpSum([contsi[k] * amount[k] for k in range(K)]) >= si_min * n_steel_quant, "Si_Min_Content"
problem += pulp.lpSum([contsi[k] * amount[k] for k in range(K)]) <= si_max * n_steel_quant, "Si_Max_Content"

# Solve the problem
problem.solve()

# Output results
output = {
    "amount": [pulp.value(amount[k]) for k in range(K)],
    "num_mang": pulp.value(num_mang)
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')