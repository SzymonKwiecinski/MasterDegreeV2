import pulp
import json

data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}

# Extracting parameters from the data
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

# Objective Function
total_profit = pulp.lpSum([
    (selling_price - material_cost) * (regular_baskets[w] + overtime_baskets[w]) - \
    (regular_used[w] * regular_cost + overtime_used[w] * overtime_cost) - \
    (holding_cost * inventory[w] if w < W - 1 else 0)
    for w in range(W)
])
total_profit += pulp.lpSum([salvage_value * inventory[W - 1]])  # Add salvage value for week W
problem += total_profit

# Constraints
for w in range(W):
    # Labor hour constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w]

    # Basket assembly constraints
    problem += regular_baskets[w] == regular_used[w] / assembly_time
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time

    # Demand constraints
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] == demand[w]
    else:
        problem += regular_baskets[w] + overtime_baskets[w] + inventory[w - 1] == demand[w] + inventory[w]

    # Update inventory for next week
    if w < W - 1:
        problem += inventory[w] == inventory[w - 1] + regular_baskets[w] + overtime_baskets[w] - demand[w]

# Solve the problem
problem.solve()

# Output results
regular_used_values = [pulp.value(regular_used[w]) for w in range(W)]
overtime_used_values = [pulp.value(overtime_used[w]) for w in range(W)]
regular_baskets_values = [pulp.value(regular_baskets[w]) for w in range(W)]
overtime_baskets_values = [pulp.value(overtime_baskets[w]) for w in range(W)]
inventory_values = [pulp.value(inventory[w]) for w in range(W)]
total_profit_value = pulp.value(problem.objective)

output = {
    "regular_used": regular_used_values,
    "overtime_used": overtime_used_values,
    "regular_baskets": regular_baskets_values,
    "overtime_baskets": overtime_baskets_values,
    "inventory": inventory_values,
    "total_profit": total_profit_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')