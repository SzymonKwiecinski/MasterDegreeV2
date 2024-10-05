import pulp

# Parse the input data
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

W = len(data['demand'])

# Initialize the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(W)]

# Objective function
total_profit = pulp.lpSum([
    data['selling_price'] * (regular_baskets[w] + overtime_baskets[w]) -
    data['material_cost'] * (regular_baskets[w] + overtime_baskets[w]) -
    data['regular_cost'] * regular_used[w] -
    data['overtime_cost'] * overtime_used[w] -
    data['holding_cost'] * (inventory[w] if w < W-1 else 0) +
    (data['salvage_value'] * inventory[w] if w == W-1 else 0)
    for w in range(W)
])

problem += total_profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]

    # Calculate the number of baskets directly based on labor used
    problem += regular_baskets[w] * data['assembly_time'] == regular_used[w]
    problem += overtime_baskets[w] * data['assembly_time'] == overtime_used[w]

    baskets_produced = regular_baskets[w] + overtime_baskets[w]
    if w == 0:
        problem += baskets_produced >= data['demand'][w] + inventory[w]
    else:
        problem += baskets_produced + inventory[w-1] == data['demand'][w] + inventory[w]

# Solve the problem
problem.solve()

# Collect the results
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