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

# Parameters
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
problem = pulp.LpProblem("FineFoodsGiftBasketProduction", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(1, W+1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(1, W+1), lowBound=0)
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(1, W+1), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(1, W+1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W+1), lowBound=0)

# Objective Function
problem += pulp.lpSum([
    (selling_price * (regular_basket[w] + overtime_basket[w]) -
     material_cost * (regular_basket[w] + overtime_basket[w]) -
     regular_cost * regular_used[w] -
     overtime_cost * overtime_used[w] -
     holding_cost * inventory[w] +
     (salvage_value if w == W else 0) * inventory[w])
    for w in range(1, W+1)
]), "Total_Profit"

# Constraints
for w in range(1, W+1):
    # Labor Constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w-1] + overtime_labor[w-1], f"Total_Labor_Week_{w}"
    problem += regular_used[w] <= regular_labor[w-1], f"Regular_Labor_Week_{w}"
    problem += overtime_used[w] <= overtime_labor[w-1], f"Overtime_Labor_Week_{w}"
    
    # Basket Production Constraints
    problem += regular_basket[w] == regular_used[w] / assembly_time, f"Regular_Basket_Prod_Week_{w}"
    problem += overtime_basket[w] == overtime_used[w] / assembly_time, f"Overtime_Basket_Prod_Week_{w}"
    
    # Demand Satisfaction and Inventory Balance
    if w == 1:
        problem += regular_basket[w] + overtime_basket[w] + 0 >= demand[w-1], f"Demand_Satisfaction_Week_{w}"
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - demand[w-1], f"Inventory_Balance_Week_{w}"
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] >= demand[w-1], f"Demand_Satisfaction_Week_{w}"
        problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - demand[w-1], f"Inventory_Balance_Week_{w}"

# Final Inventory Salvage
problem += inventory[W] >= 0, "Final_Inventory_Salvage"

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')