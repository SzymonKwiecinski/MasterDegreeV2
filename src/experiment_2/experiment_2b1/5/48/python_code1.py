import pulp
import json

data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 
        'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 
        'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 
        'regular_labor': [450, 550, 600, 600], 
        'overtime_labor': [40, 200, 320, 160]}

W = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=data['regular_labor'][w]) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=data['overtime_labor'][w]) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(W)]

# Objective function
profit = pulp.lpSum([(data['selling_price'] - data['material_cost'] - (data['regular_cost'] * regular_used[w] + data['overtime_cost'] * overtime_used[w]) / data['assembly_time'] 
                      - (data['holding_cost'] * inventory[w] if w < W - 1 else 0)) 
                      for w in range(W)]) 
profit += pulp.lpSum([data['salvage_value'] * inventory[-1]])  # Only salvage on last week's inventory
problem += profit

# Constraints
for w in range(W):
    # Demand constraints
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] == data['demand'][w]
        problem += inventory[w] == 0  # No initial inventory
    else:
        problem += regular_baskets[w] + overtime_baskets[w] + inventory[w-1] == data['demand'][w] + inventory[w]

    # Labor constraints
    problem += regular_used[w] / data['assembly_time'] <= regular_baskets[w]
    problem += overtime_used[w] / data['assembly_time'] <= overtime_baskets[w]

# Solve the problem
problem.solve()

# Collect results
regular_used_values = [pulp.value(regular_used[w]) for w in range(W)]
overtime_used_values = [pulp.value(overtime_used[w]) for w in range(W)]
regular_baskets_values = [pulp.value(regular_baskets[w]) for w in range(W)]
overtime_baskets_values = [pulp.value(overtime_baskets[w]) for w in range(W)]
inventory_values = [pulp.value(inventory[w]) for w in range(W)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "regular_used": regular_used_values,
    "overtime_used": overtime_used_values,
    "regular_baskets": regular_baskets_values,
    "overtime_baskets": overtime_baskets_values,
    "inventory": inventory_values,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')