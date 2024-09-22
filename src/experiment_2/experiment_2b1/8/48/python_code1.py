import pulp
import json

data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 
        'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 
        'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 
        'regular_labor': [450, 550, 600, 600], 
        'overtime_labor': [40, 200, 320, 160]}

# Extracting data from JSON-like input
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

# Create the problem
problem = pulp.LpProblem("GiftBasketsMaxProfit", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=regular_labor[w]) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=overtime_labor[w]) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(W)]

# Objective Function: Maximize total profit
total_revenue = sum((regular_baskets[w] + overtime_baskets[w]) * selling_price for w in range(W))
total_cost = sum(regular_used[w] * regular_cost + overtime_used[w] * overtime_cost + 
                 inventory[w] * holding_cost for w in range(W)) - inventory[W-1] * salvage_value
objective_function = total_revenue - total_cost
problem += objective_function, "Total Profit"

# Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w], f"Labor_Constraint_{w}"
    problem += regular_baskets[w] + overtime_baskets[w] + (inventory[w-1] if w > 0 else 0) == demand[w] + inventory[w], f"Demand_Constraint_{w}"

# Inventory at week W
problem += inventory[W-1] == (regular_baskets[W-1] + overtime_baskets[W-1]) - demand[W-1], "Final_Inventory_Constraint"

# Solve the problem
problem.solve()

# Prepare result
result = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')