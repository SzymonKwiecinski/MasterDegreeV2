import pulp
import json

# Input data
data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25,
        'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30,
        'demand': [700, 1500, 2800, 1800], 
        'regular_labor': [450, 550, 600, 600], 
        'overtime_labor': [40, 200, 320, 160]}

W = len(data['demand'])

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=data['regular_labor'][w-1]) for w in range(1, W + 1)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=data['overtime_labor'][w-1]) for w in range(1, W + 1)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(1, W + 1)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(1, W + 1)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(1, W + 1)]

# Objective function
profit = pulp.lpSum([
    (data['selling_price'] - data['material_cost'] - (data['regular_cost'] * (regular_used[w-1] / data['assembly_time']) if regular_used[w-1] > 0 else 0) - (data['overtime_cost'] * (overtime_used[w-1] / data['assembly_time']) if overtime_used[w-1] > 0 else 0)) * (regular_baskets[w-1] + overtime_baskets[w-1])
    for w in range(1, W + 1)
])

holding_costs = pulp.lpSum([
    data['holding_cost'] * inventory[w-1]
    for w in range(1, W + 1)
])

salvage_values = pulp.lpSum([
    data['salvage_value'] * inventory[W - 1]
])

total_profit = profit - holding_costs + salvage_values

problem += total_profit

# Constraints
for w in range(1, W + 1):
    if w == 1:
        problem += regular_baskets[w-1] + overtime_baskets[w-1] == data['demand'][w-1]
    else:
        problem += regular_baskets[w-1] + overtime_baskets[w-1] + inventory[w-2] == data['demand'][w-1]

    problem += regular_used[w-1] + overtime_used[w-1] == (regular_baskets[w-1] + overtime_baskets[w-1]) * data['assembly_time']

    if w < W:
        problem += inventory[w-1] == inventory[w-2] + regular_baskets[w-1] + overtime_baskets[w-1] - data['demand'][w-1]
    else:
        problem += inventory[w-1] == inventory[w-2] + regular_baskets[w-1] + overtime_baskets[w-1] - data['demand'][w-1]

# Solve the problem
problem.solve()

# Collect results
result = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

# Output the result
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')