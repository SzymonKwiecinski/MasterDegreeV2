import pulp
import json

data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}

W = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("GiftBasketProduction", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0, upBound=None)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0, upBound=None)
regular_basket = pulp.LpVariable.dicts("RegularBaskets", range(W), lowBound=0, upBound=None, cat='Integer')
overtime_basket = pulp.LpVariable.dicts("OvertimeBaskets", range(W), lowBound=0, upBound=None, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0, upBound=None)

# Objective Function
profit = pulp.lpSum([
    (data['selling_price'] - data['material_cost']) * (regular_basket[w] + overtime_basket[w]) - \
    data['regular_cost'] * regular_used[w] - data['overtime_cost'] * overtime_used[w] - \
    data['holding_cost'] * inventory[w] for w in range(W)
])
profit += pulp.lpSum([(data['salvage_value'] * inventory[W-1])])  # Salvage value for unsold baskets in last week
problem += profit

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w]
    
    # Production constraints
    problem += regular_basket[w] * data['assembly_time'] <= regular_used[w]
    problem += overtime_basket[w] * data['assembly_time'] <= overtime_used[w]
    
    # Demand satisfaction and inventory constraints
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] == data['demand'][w], f"DemandWeek{w+1}"
        inventory[w] == 0
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] - data['demand'][w] == inventory[w], f"InventoryWeek{w+1}"
    
    # Inventory non-negativity
    problem += inventory[w] >= 0

# Solve the problem
problem.solve()

# Extract results
regular_used_result = [regular_used[w].varValue for w in range(W)]
overtime_used_result = [overtime_used[w].varValue for w in range(W)]
regular_baskets_result = [regular_basket[w].varValue for w in range(W)]
overtime_baskets_result = [overtime_basket[w].varValue for w in range(W)]
inventory_result = [inventory[w].varValue for w in range(W)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "regular_used": regular_used_result,
    "overtime_used": overtime_used_result,
    "regular_baskets": regular_baskets_result,
    "overtime_baskets": overtime_baskets_result,
    "inventory": inventory_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')