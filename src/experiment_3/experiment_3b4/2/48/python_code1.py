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

W = len(data['demand'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("regular_used", list(range(W)), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("overtime_used", list(range(W)), lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts("regular_basket", list(range(W)), lowBound=0, cat='Continuous')
overtime_basket = pulp.LpVariable.dicts("overtime_basket", list(range(W)), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", list(range(W+1)), lowBound=0, cat='Continuous')

# Initial Inventory
problem += (inventory[0] == 0, "Initial_Inventory")

# Constraints
for w in range(W):
    # Labor constraints
    problem += (regular_used[w] <= data['regular_labor'][w], f"Regular_Labor_Week_{w}")
    problem += (overtime_used[w] <= data['overtime_labor'][w], f"Overtime_Labor_Week_{w}")
    
    # Basket assembly
    problem += (regular_basket[w] == regular_used[w] * (1 / data['assembly_time']), f"Regular_Basket_Week_{w}")  # fixed here
    problem += (overtime_basket[w] == overtime_used[w] * (1 / data['assembly_time']), f"Overtime_Basket_Week_{w}")  # fixed here
    
    # Inventory balance
    if w == 0:
        problem += (inventory[w+1] == regular_basket[w] + overtime_basket[w] - data['demand'][w], f"Inventory_Balance_Week_{w}")
    else:
        problem += (inventory[w+1] == inventory[w] + regular_basket[w] + overtime_basket[w] - data['demand'][w], f"Inventory_Balance_Week_{w}")

# Objective Function
total_profit = pulp.lpSum([
    data['selling_price'] * (regular_basket[w] + overtime_basket[w])
    - data['regular_cost'] * regular_used[w]
    - data['overtime_cost'] * overtime_used[w]
    - data['material_cost'] * (regular_basket[w] + overtime_basket[w])
    - (data['holding_cost'] * inventory[w] if w < W-1 else 0)
    for w in range(W)
]) + data['salvage_value'] * inventory[W]

problem += total_profit

# Solve
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')