import pulp

# Data input from JSON format
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

# Extract data
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
demands = data['demand']
regular_labors = data['regular_labor']
overtime_labors = data['overtime_labor']

W = len(demands)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_baskets_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_baskets_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(W)]

# Objective
profit = pulp.lpSum(
    (selling_price - material_cost) * (regular_baskets[w] + overtime_baskets[w])
    - regular_cost * regular_used[w]
    - overtime_cost * overtime_used[w]
    - holding_cost * inventory[w]
    for w in range(W)
) + salvage_value * inventory[-1]

problem += profit, "Total_Profit"

# Constraints
for w in range(W):
    problem += regular_used[w] <= regular_labors[w], f"Regular_Labor_Limit_{w}"
    problem += overtime_used[w] <= overtime_labors[w], f"Overtime_Labor_Limit_{w}"
    problem += regular_baskets[w] == regular_used[w] / assembly_time, f"Regular_Basket_Production_{w}"
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time, f"Overtime_Basket_Production_{w}"
    
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] == demands[w] + inventory[w], f"Demand_Fulfillment_Week_{w}"
    else:
        problem += regular_baskets[w] + overtime_baskets[w] + inventory[w-1] == demands[w] + inventory[w], f"Demand_Fulfillment_Week_{w}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    'regular_used': [pulp.value(regular_used[w]) for w in range(W)],
    'overtime_used': [pulp.value(overtime_used[w]) for w in range(W)],
    'regular_baskets': [pulp.value(regular_baskets[w]) for w in range(W)],
    'overtime_baskets': [pulp.value(overtime_baskets[w]) for w in range(W)],
    'inventory': [pulp.value(inventory[w]) for w in range(W)],
    'total_profit': pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')