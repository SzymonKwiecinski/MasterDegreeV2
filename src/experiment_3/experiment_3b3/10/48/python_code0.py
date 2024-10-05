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

# Number of weeks
W = len(data['demand'])

# Initialize the problem
problem = pulp.LpProblem("Gift_Baskets_Assembly_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
regular_used = {w: pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)}
overtime_used = {w: pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)}
regular_baskets = {w: pulp.LpVariable(f'regular_baskets_{w}', lowBound=0) for w in range(W)}
overtime_baskets = {w: pulp.LpVariable(f'overtime_baskets_{w}', lowBound=0) for w in range(W)}
inventory = {w: pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)}

# Objective Function
problem += pulp.lpSum(
    (data['selling_price'] - data['material_cost']) * (regular_baskets[w] + overtime_baskets[w]) - 
    data['regular_cost'] * regular_used[w] - 
    data['overtime_cost'] * overtime_used[w] - 
    data['holding_cost'] * inventory[w] for w in range(W)
) + data['salvage_value'] * inventory[W-1], "Total Profit"

# Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w], f"Labor Constraint {w}"

    problem += regular_baskets[w] == regular_used[w] / data['assembly_time'], f"Regular Baskets Production {w}"
    problem += overtime_baskets[w] == overtime_used[w] / data['assembly_time'], f"Overtime Baskets Production {w}"
    
    if w == 0:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - data['demand'][w], f"Inventory Balance {w}"
    else:
        problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w], f"Inventory Balance {w}"

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')