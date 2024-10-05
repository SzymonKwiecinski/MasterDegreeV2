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

# Parameters
W = len(data['demand'])
assembly_time = data['assembly_time']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w+1}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w+1}', lowBound=0) for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w+1}', lowBound=0, cat='Integer') for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w+1}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w+1}', lowBound=0, cat='Integer') for w in range(W)]

# Objective Function: Maximize total profit
profit = pulp.lpSum(
    (selling_price - material_cost) * (regular_basket[w] + overtime_basket[w]) 
    - regular_cost * regular_used[w] 
    - overtime_cost * overtime_used[w] 
    - holding_cost * inventory[w] 
    for w in range(W)
)

# Add salvage value for unsold inventory at end
profit += salvage_value * inventory[-1]
problem += profit, "Total Profit"

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] <= regular_labor[w], f"Regular_Labor_Limit_{w+1}"
    problem += overtime_used[w] <= overtime_labor[w], f"Overtime_Labor_Limit_{w+1}"
    
    # Basket assembly constraints
    problem += regular_basket[w] <= regular_used[w] / assembly_time, f"Regular_Basket_Assembly_{w+1}"
    problem += overtime_basket[w] <= overtime_used[w] / assembly_time, f"Overtime_Basket_Assembly_{w+1}"
    
    # Demand and inventory balance
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] == demand[w] + inventory[w], f"Demand_Fulfillment_{w+1}"
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] == demand[w] + inventory[w], f"Demand_Fulfillment_{w+1}"

# Solve the problem
problem.solve()

# Preparing output data
regular_used_vals = [pulp.value(regular_used[w]) for w in range(W)]
overtime_used_vals = [pulp.value(overtime_used[w]) for w in range(W)]
regular_basket_vals = [pulp.value(regular_basket[w]) for w in range(W)]
overtime_basket_vals = [pulp.value(overtime_basket[w]) for w in range(W)]
inventory_vals = [pulp.value(inventory[w]) for w in range(W)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "regular_used": regular_used_vals,
    "overtime_used": overtime_used_vals,
    "regular_baskets": regular_basket_vals,
    "overtime_baskets": overtime_basket_vals,
    "inventory": inventory_vals,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')