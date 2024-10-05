import pulp

# Data from input
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

W = len(data['demand'])  # number of weeks

# Define the Linear Programming problem
problem = pulp.LpProblem("Gift_Baskets_Profit_Maximization", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_baskets_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_baskets_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(W)]

# Objective function
total_revenue = pulp.lpSum((data['selling_price'] * (regular_baskets[w] + overtime_baskets[w])) for w in range(W))
total_regular_cost = pulp.lpSum((data['regular_cost'] * regular_used[w]) for w in range(W))
total_overtime_cost = pulp.lpSum((data['overtime_cost'] * overtime_used[w]) for w in range(W))
total_material_cost = pulp.lpSum((data['material_cost'] * (regular_baskets[w] + overtime_baskets[w])) for w in range(W))
total_holding_cost = pulp.lpSum((data['holding_cost'] * inventory[w]) for w in range(W-1))
salvage_value = pulp.lpSum((data['salvage_value'] * inventory[W-1]))

# Objective function
problem += (total_revenue + salvage_value - total_regular_cost - total_overtime_cost - total_material_cost - total_holding_cost)

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]

    # Production constraints
    problem += regular_baskets[w] == regular_used[w] / data['assembly_time']
    problem += overtime_baskets[w] == overtime_used[w] / data['assembly_time']

    # Inventory balance constraints
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] - inventory[w] == data['demand'][w]
    else:
        problem += regular_baskets[w] + overtime_baskets[w] + inventory[w-1] - inventory[w] == data['demand'][w]

# Solve the problem
problem.solve()

# Output the solution
output = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(output)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')