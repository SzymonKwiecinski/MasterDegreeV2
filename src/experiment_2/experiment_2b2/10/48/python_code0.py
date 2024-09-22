import pulp

# Data from JSON
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

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=regular_labor[w], cat='Continuous') for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=overtime_labor[w], cat='Continuous') for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Continuous') for w in range(W)]

# Profit calculation
revenue = [selling_price * (regular_basket[w] + overtime_basket[w]) for w in range(W)]
regular_costs = [regular_cost * regular_used[w] for w in range(W)]
overtime_costs = [overtime_cost * overtime_used[w] for w in range(W)]
material_costs = [material_cost * (regular_basket[w] + overtime_basket[w]) for w in range(W)]
holding_costs = [holding_cost * inventory[w] for w in range(W)]
salvage = salvage_value * inventory[-1]

# Objective function
total_profit = pulp.lpSum(revenue) - pulp.lpSum(regular_costs) - pulp.lpSum(overtime_costs) - pulp.lpSum(material_costs) - pulp.lpSum(holding_costs) + salvage
problem += total_profit

# Constraints
for w in range(W):
    # Regular and overtime labor constraints
    problem += regular_used[w] >= assembly_time * regular_basket[w], f'Regular_Labor_Constraint_{w}'
    problem += overtime_used[w] >= assembly_time * overtime_basket[w], f'Overtime_Labor_Constraint_{w}'
    
    # Inventory balance
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] == demand[w] + inventory[w], f'Demand_Constraint_{w}'
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] == demand[w] + inventory[w], f'Demand_Constraint_{w}'

# Solve the problem
problem.solve()

# Collect results
output = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_basket[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_basket[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')