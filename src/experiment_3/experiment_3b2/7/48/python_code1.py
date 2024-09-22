import pulp

# Define the data
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

W = len(data['demand'])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W + 1), lowBound=0)

# Objective Function
total_profit = pulp.lpSum([
    data['selling_price'] * (regular_basket[w] + overtime_basket[w]) -
    data['regular_cost'] * regular_used[w] -
    data['overtime_cost'] * overtime_used[w] -
    data['material_cost'] * (regular_basket[w] + overtime_basket[w]) -
    data['holding_cost'] * inventory[w]
    for w in range(W)
]) + data['salvage_value'] * inventory[W]

problem += total_profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w], f"RegularLaborLimit_{w}"
    problem += overtime_used[w] <= data['overtime_labor'][w], f"OvertimeLaborLimit_{w}"
    problem += regular_basket[w] == regular_used[w] / data['assembly_time'], f"RegularBasketAssembly_{w}"
    problem += overtime_basket[w] == overtime_used[w] / data['assembly_time'], f"OvertimeBasketAssembly_{w}"

    if w == 0:
        problem += inventory[w] == 0, f"InitialInventory_{w}"
    else:
        problem += inventory[w] == inventory[w - 1] + regular_basket[w] + overtime_basket[w] - data['demand'][w], f"InventoryBalance_{w}"

    problem += inventory[w] >= 0, f"InventoryNonNegativity_{w}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')