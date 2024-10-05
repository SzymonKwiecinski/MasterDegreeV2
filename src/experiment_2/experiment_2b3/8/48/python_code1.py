import pulp

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

# Constants
weeks = len(data['demand'])
assembly_time = data['assembly_time']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
selling_price = data['selling_price']
material_cost = data['material_cost']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

# Decision variables
problem = pulp.LpProblem("Gift_Basket_Problem", pulp.LpMaximize)

regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(weeks)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(weeks)]
regular_baskets = [pulp.LpVariable(f'regular_baskets_{w}', lowBound=0, cat='Integer') for w in range(weeks)]
overtime_baskets = [pulp.LpVariable(f'overtime_baskets_{w}', lowBound=0, cat='Integer') for w in range(weeks)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(weeks)]

# Objective function
total_revenue = pulp.lpSum((regular_baskets[w] + overtime_baskets[w]) * (selling_price - material_cost) for w in range(weeks))
total_regular_cost = pulp.lpSum(regular_used[w] * regular_cost for w in range(weeks))
total_overtime_cost = pulp.lpSum(overtime_used[w] * overtime_cost for w in range(weeks))
total_holding_cost = pulp.lpSum(inventory[w] * holding_cost for w in range(weeks - 1))
total_salvage_value = inventory[weeks - 1] * salvage_value

problem += total_revenue - total_regular_cost - total_overtime_cost - total_holding_cost + total_salvage_value

# Constraints
for w in range(weeks):
    problem += regular_used[w] <= data['regular_labor'][w], f'Regular Labor Limit {w}'
    problem += overtime_used[w] <= data['overtime_labor'][w], f'Overtime Labor Limit {w}'
    problem += regular_baskets[w] == regular_used[w] / assembly_time, f'Regular Basket Production {w}'
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time, f'Overtime Basket Production {w}'
    
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] == data['demand'][w], f'Demand Balance {w}'
    else:
        problem += regular_baskets[w] + overtime_baskets[w] + inventory[w - 1] == data['demand'][w] + inventory[w], f'Demand Balance {w}'

# Solve the problem
problem.solve()

# Output the results
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