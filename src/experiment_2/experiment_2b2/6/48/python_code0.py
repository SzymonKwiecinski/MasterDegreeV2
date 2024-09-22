import pulp

# Data input
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

# Unpack data
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
W = len(demand)

# Problem formulation
problem = pulp.LpProblem("GiftBasketProduction", pulp.LpMaximize)

# Variables
regular_used = [pulp.LpVariable(f"regular_used_{w}", 0, regular_labor[w]) for w in range(W)]
overtime_used = [pulp.LpVariable(f"overtime_used_{w}", 0, overtime_labor[w]) for w in range(W)]
regular_baskets = [pulp.LpVariable(f"regular_basket_{w}", 0) for w in range(W)]
overtime_baskets = [pulp.LpVariable(f"overtime_basket_{w}", 0) for w in range(W)]
inventory = [pulp.LpVariable(f"inventory_{w}", 0) for w in range(W)]

# Constraints
for w in range(W):
    problem += regular_baskets[w] == regular_used[w] / assembly_time, f"RegularBasketProduction_{w}"
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time, f"OvertimeBasketProduction_{w}"
    if w == 0:
        problem += inventory[w] == (regular_baskets[w] + overtime_baskets[w]) - demand[w], f"InventoryBalance_{w}"
    else:
        problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - demand[w], f"InventoryBalance_{w}"

# Objective function
profit = pulp.lpSum([
    selling_price * (regular_baskets[w] + overtime_baskets[w]) 
    - material_cost * (regular_baskets[w] + overtime_baskets[w])
    - regular_cost * regular_used[w]
    - overtime_cost * overtime_used[w]
    - holding_cost * inventory[w]
    for w in range(W)
]) + salvage_value * inventory[-1]

problem += profit

# Solve
problem.solve()

# Output
output = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')