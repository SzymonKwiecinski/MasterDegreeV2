import pulp

# Data provided
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

# Extracting values
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

# Initialize problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=regular_labor[w], cat='Continuous') for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=overtime_labor[w], cat='Continuous') for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Continuous') for w in range(W)]

# Constraints
for w in range(W):
    problem += regular_basket[w] == regular_used[w] / assembly_time
    problem += overtime_basket[w] == overtime_used[w] / assembly_time
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] >= demand[w] + inventory[w]
    else:
        problem += inventory[w-1] + regular_basket[w] + overtime_basket[w] >= demand[w] + inventory[w]

# Objective function
profit = pulp.lpSum([
    (selling_price * (regular_basket[w] + overtime_basket[w])) - 
    (material_cost * (regular_basket[w] + overtime_basket[w])) - 
    (holding_cost * inventory[w] if w < W-1 else 0) - 
    (regular_cost * regular_used[w]) - 
    (overtime_cost * overtime_used[w]) 
    for w in range(W)
])
# Add salvage value for the last week's inventory
profit += salvage_value * inventory[W-1]

problem += profit

# Solve the problem
problem.solve()

# Output the results
results = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_basket[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_basket[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

# Print the results
print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')