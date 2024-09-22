import json
import pulp

data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}

# Extracting data from JSON
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=regular_labor[w-1]) for w in range(1, W+1)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=overtime_labor[w-1]) for w in range(1, W+1)]
regular_baskets = [pulp.LpVariable(f'regular_baskets_{w}', lowBound=0, cat='Integer') for w in range(1, W+1)]
overtime_baskets = [pulp.LpVariable(f'overtime_baskets_{w}', lowBound=0, cat='Integer') for w in range(1, W+1)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(1, W+1)]

# Objective Function
total_profit = pulp.lpSum(
    (selling_price - material_cost) * (regular_baskets[w] + overtime_baskets[w]) -
    (regular_cost * (regular_used[w] / assembly_time) + overtime_cost * (overtime_used[w] / assembly_time)) -
    holding_cost * inventory[w] for w in range(W)
)
total_profit += pulp.lpSum(
    salvage_value * inventory[W-1]
)
problem += total_profit

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w], f"Labor_Constraint_{w+1}"
    
    # Production constraints
    problem += regular_baskets[w] + overtime_baskets[w] == (regular_used[w] + overtime_used[w]) / assembly_time, f"Production_Constraint_{w+1}"
    
    # Inventory balance constraints
    if w == 0:
        problem += inventory[w] == demand[w] - (regular_baskets[w] + overtime_baskets[w]), f"Inventory_Balance_{w+1}"
    else:
        problem += inventory[w] == inventory[w-1] + demand[w] - (regular_baskets[w] + overtime_baskets[w]), f"Inventory_Balance_{w+1}"

# Last week inventory does not incur holding cost
problem += inventory[W-1] >= 0, "Final_Inventory_Zero"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')