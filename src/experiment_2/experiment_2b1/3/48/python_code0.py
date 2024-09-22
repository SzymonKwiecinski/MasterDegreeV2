import pulp
import json

# Input data
data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}

W = len(data['demand'])

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=data['regular_labor'][w]) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=data['overtime_labor'][w]) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

# Objective function
total_profit = sum((data['selling_price'] - data['material_cost']) * (regular_baskets[w] + overtime_baskets[w]) - data['regular_cost'] * regular_used[w] - data['overtime_cost'] * overtime_used[w] for w in range(W))
total_profit -= sum(data['holding_cost'] * inventory[w] for w in range(W - 1))  # holding costs for weeks 1 to W-1
total_profit += (data['salvage_value'] * inventory[W - 1])  # salvage value for week W
problem += total_profit

# Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] >= (regular_baskets[w] + overtime_baskets[w]) * data['assembly_time'], f"Assembly_time_constraint_{w}"
    
    # Inventory balance
    if w == 0:
        problem += inventory[w] == (regular_baskets[w] + overtime_baskets[w]) - data['demand'][w], f"Inventory_balance_week_{w}"
    else:
        problem += inventory[w] == inventory[w - 1] + (regular_baskets[w] + overtime_baskets[w]) - data['demand'][w], f"Inventory_balance_week_{w}"

# Solve the problem
problem.solve()

# Prepare the results
results = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

# Output the results
print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')