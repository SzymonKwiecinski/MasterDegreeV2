import pulp
import json

data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}

W = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(W), lowBound=0, cat='Integer')
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

# Objective Function
profit = pulp.lpSum((data['selling_price'] - data['material_cost']) * (regular_baskets[w] + overtime_baskets[w]) 
                    - data['regular_cost'] * regular_used[w] 
                    - data['overtime_cost'] * overtime_used[w] 
                    - data['holding_cost'] * inventory[w] for w in range(W))

problem += profit

# Constraints
for w in range(W):
    # Labor constraint
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w]

    # Production based on labor
    problem += regular_baskets[w] == regular_used[w] / data['assembly_time']
    problem += overtime_baskets[w] == overtime_used[w] / data['assembly_time']
    
    # Inventory balance
    if w == 0:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - data['demand'][w]
    else:
        problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w]

# Salvage for the last week
problem += inventory[W-1] == inventory[W-1] + data['salvage_value'] * (inventory[W-1] > 0)

# Solve the problem
problem.solve()

# Output results
regular_used_solution = [pulp.value(regular_used[w]) for w in range(W)]
overtime_used_solution = [pulp.value(overtime_used[w]) for w in range(W)]
regular_baskets_solution = [pulp.value(regular_baskets[w]) for w in range(W)]
overtime_baskets_solution = [pulp.value(overtime_baskets[w]) for w in range(W)]
inventory_solution = [pulp.value(inventory[w]) for w in range(W)]
total_profit = pulp.value(problem.objective)

output = {
    "regular_used": regular_used_solution,
    "overtime_used": overtime_used_solution,
    "regular_baskets": regular_baskets_solution,
    "overtime_baskets": overtime_baskets_solution,
    "inventory": inventory_solution,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')