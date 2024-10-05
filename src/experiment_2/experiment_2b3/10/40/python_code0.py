import pulp

# Parse the input data
data = {
    "n_steel_quant": 1000,
    "mn_percent": 0.45,
    "si_min": 3.25,
    "si_max": 5.0,
    "contsi": [4.0, 1.0, 0.6],
    "contmn": [0.45, 0.5, 0.4],
    "mang_price": 8.0,
    "cost": [21, 25, 15],
    "sell_price": 0.45,
    "melt_price": 0.005
}

# Extract data
n_steel_quant = data["n_steel_quant"]
mn_percent = data["mn_percent"]
si_min = data["si_min"]
si_max = data["si_max"]
contsi = data["contsi"]
contmn = data["contmn"]
mang_price = data["mang_price"]
cost = data["cost"]
sell_price = data["sell_price"]
melt_price = data["melt_price"]
num_minerals = len(contsi)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(num_minerals)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective function
total_revenue = sell_price * n_steel_quant
total_cost = sum((cost[k] / 1000 + melt_price) * amount[k] for k in range(num_minerals))
total_cost += mang_price * num_mang
profit = total_revenue - total_cost
problem += profit

# Constraints
# Constraint for total steel production
problem += pulp.lpSum(amount) + num_mang == n_steel_quant

# Constraint for manganese content
problem += pulp.lpSum(contmn[k] * amount[k] for k in range(num_minerals)) + num_mang >= mn_percent * n_steel_quant

# Constraint for silicon content between bounds
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(num_minerals)) >= si_min * n_steel_quant
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(num_minerals)) <= si_max * n_steel_quant

# Solve the problem
problem.solve()

# Extract results
result_amount = [pulp.value(amount[k]) for k in range(num_minerals)]
result_num_mang = pulp.value(num_mang)

# Output results
output = {
    "amount": result_amount,
    "num_mang": [result_num_mang]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')