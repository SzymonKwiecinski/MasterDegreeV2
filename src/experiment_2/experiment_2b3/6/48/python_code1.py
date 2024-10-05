import pulp

# Data
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

# Variables
W = len(data['demand'])
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

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_hours = pulp.LpVariable.dicts("Regular_Hours", range(W), lowBound=0)
overtime_hours = pulp.LpVariable.dicts("Overtime_Hours", range(W), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("Regular_Baskets", range(W), lowBound=0, cat='Integer')
overtime_baskets = pulp.LpVariable.dicts("Overtime_Baskets", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum([
    (selling_price - material_cost) * (regular_baskets[w] + overtime_baskets[w]) -
    (regular_cost * regular_hours[w]) -
    (overtime_cost * overtime_hours[w]) -
    (holding_cost * inventory[w]) +
    (salvage_value * inventory[W-1] if w == W-1 else 0)
    for w in range(W)
])

problem += profit

# Constraints
for w in range(W):
    problem += regular_hours[w] <= regular_labor[w]
    problem += overtime_hours[w] <= overtime_labor[w]

    problem += regular_baskets[w] == regular_hours[w] / assembly_time
    problem += overtime_baskets[w] == overtime_hours[w] / assembly_time

    if w == 0:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - demand[w]
    else:
        problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - demand[w]

# Solve
problem.solve()

# Output
output = {
    "regular_used": [pulp.value(regular_hours[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_hours[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')