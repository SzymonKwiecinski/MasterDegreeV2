import pulp
import json

# Input data
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

# Problem setup
W = len(data['demand'])
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=data['regular_labor'][w-1]) for w in range(1, W+1)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=data['overtime_labor'][w-1]) for w in range(1, W+1)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Integer') for w in range(1, W+1)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Integer') for w in range(1, W+1)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(1, W+1)]

# Objective function
total_profit = pulp.lpSum([
    (data['selling_price'] - data['material_cost']) * (regular_baskets[w] + overtime_baskets[w]) - \
    (data['regular_cost'] * regular_used[w] + data['overtime_cost'] * overtime_used[w]) - \
    data['holding_cost'] * inventory[w] 
    for w in range(W)
]) + pulp.lpSum([
    (data['salvage_value'] * inventory[W-1]) 
])

problem += total_profit

# Constraints

# Demand and inventory constraints
for w in range(W):
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] == data['demand'][w], f'demand_ct_{w+1}'
        problem += inventory[w] == 0, f'inv_ct_start_{w+1}'
    else:
        problem += inventory[w-1] + regular_baskets[w] + overtime_baskets[w] == data['demand'][w] + inventory[w], f'demand_ct_{w+1}'

# Regular and overtime labor constraints
for w in range(W):
    problem += regular_used[w] / data['assembly_time'] + overtime_used[w] / data['assembly_time'] >= regular_baskets[w] + overtime_baskets[w], f'labor_ct_{w+1}'

# Inventory balance
for w in range(W-1):
    problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w], f'inventory_balance_{w+1}'

# Solve the problem
problem.solve()

# Output the results
results = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')