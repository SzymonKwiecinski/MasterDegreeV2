import pulp
import json

# Input data
data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 
        'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 
        'demand': [700, 1500, 2800, 1800], 
        'regular_labor': [450, 550, 600, 600], 
        'overtime_labor': [40, 200, 320, 160]}

W = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(W), lowBound=0, cat='Integer')
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

# Objective function
profit = pulp.lpSum((data['selling_price'] - data['material_cost']) * (regular_baskets[w] + overtime_baskets[w]) 
                    - data['regular_cost'] * regular_used[w] 
                    - data['overtime_cost'] * overtime_used[w] 
                    - data['holding_cost'] * inventory[w] 
                    for w in range(W))
problem += profit

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w], f"LaborConstraint_{w}"
    
    # Baskets produced constraints
    problem += regular_baskets[w] == regular_used[w] / data['assembly_time'], f"RegularBasketsProduced_{w}"
    problem += overtime_baskets[w] == overtime_used[w] / data['assembly_time'], f"OvertimeBasketsProduced_{w}"
    
    # Inventory balance constraints
    if w == 0:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - data['demand'][w], f"InventoryBalance_{w}"
    else:
        problem += inventory[w] == inventory[w - 1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w], f"InventoryBalance_{w}"

# End of season salvage value
problem += inventory[W - 1] <= data['salvage_value'], "EndOfSeasonInventory"

# Solve the problem
problem.solve()

# Output results
output = {
    "regular_used": [regular_used[w].varValue for w in range(W)],
    "overtime_used": [overtime_used[w].varValue for w in range(W)],
    "regular_baskets": [regular_baskets[w].varValue for w in range(W)],
    "overtime_baskets": [overtime_baskets[w].varValue for w in range(W)],
    "inventory": [inventory[w].varValue for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Final output
output