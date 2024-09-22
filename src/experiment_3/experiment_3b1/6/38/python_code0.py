import pulp

# Data from JSON format
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Parameters
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Setting up the problem
problem = pulp.LpProblem("Production_Cost_Minimization", pulp.LpMinimize)

# Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
# Production Capacity Constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] <= max_regular_amount  # inventory_0 = 0
    else:
        problem += reg_quant[n] + over_quant[n] <= max_regular_amount + inventory[n-1]

# Demand Satisfaction Constraints
for n in range(N):
    problem += inventory[n] >= demand[n]

# Inventory Balance Constraints
for n in range(N):
    if n == 0:
        problem += inventory[n] == reg_quant[n] + over_quant[n] - demand[n]  # inventory_0 = 0
    else:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n]

# Solve the problem
problem.solve()

# Output the results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_values}')
print(f'Overtime Production Quantities: {over_quant_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')