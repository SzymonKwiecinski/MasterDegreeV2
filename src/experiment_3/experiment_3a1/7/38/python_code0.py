import pulp

# Data provided in JSON format
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Parameters
demand = data['demand']
N = len(demand)
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the problem
problem = pulp.LpProblem("Production_Cost_Minimization", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
problem += (inventory[0] == 0, "Initial_Inventory")

for n in range(1, N):
    problem += (inventory[n] == inventory[n - 1] + reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_{n}")

for n in range(N):
    problem += (inventory[n] >= 0, f"Non_Negative_Inventory_{n}")
    problem += (reg_quant[n] <= max_regular_amount, f"Max_Regular_Amount_{n}")

# Solve the problem
problem.solve()

# Output the results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_values}')
print(f'Overtime Production Quantities: {over_quant_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')