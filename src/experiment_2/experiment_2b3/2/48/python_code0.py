import pulp

# Problem data
data = {
    'regular_cost': 30,
    'overtime_cost': 45,
    'assembly_time': 0.4,
    'material_cost': 25,
    'selling_price': 65,
    'holding_cost': 4,
    'salvage_value': 30,
    'demand': [700, 1500, 2800, 1800],
    'regular_labor': [450, 550, 600, 600],
    'overtime_labor': [40, 200, 320, 160]
}

# Extract variables
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
demands = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
weeks = len(demands)

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w+1}', lowBound=0, upBound=regular_labor[w]) for w in range(weeks)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w+1}', lowBound=0, upBound=overtime_labor[w]) for w in range(weeks)]
regular_baskets = [pulp.LpVariable(f'regular_baskets_{w+1}', lowBound=0) for w in range(weeks)]
overtime_baskets = [pulp.LpVariable(f'overtime_baskets_{w+1}', lowBound=0) for w in range(weeks)]
inventory = [pulp.LpVariable(f'inventory_{w+1}', lowBound=0) for w in range(weeks)]

# Objective function
profit = pulp.lpSum([
    (selling_price - material_cost) * (regular_baskets[w] + overtime_baskets[w]) - 
    regular_cost * regular_used[w] - overtime_cost * overtime_used[w] - 
    holding_cost * inventory[w] for w in range(weeks)
])
# Add salvage for the last week inventory
profit += salvage_value * inventory[-1]
problem += profit

# Constraints
for w in range(weeks):
    problem += regular_baskets[w] == regular_used[w] / assembly_time, f'Regular_Baskets_Week_{w+1}'
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time, f'Overtime_Baskets_Week_{w+1}'
    demand_met = regular_baskets[w] + overtime_baskets[w] + inventory[w] - (inventory[w-1] if w > 0 else 0) >= demands[w]
    problem += demand_met, f'Demand_Met_Week_{w+1}'

# Solve the problem
problem.solve()

# Extract the results
output = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(weeks)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(weeks)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(weeks)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(weeks)],
    "inventory": [pulp.value(inventory[w]) for w in range(weeks)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')