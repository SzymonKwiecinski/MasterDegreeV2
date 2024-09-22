import pulp
import json

# Data from the provided JSON
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

# Create a linear programming problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

# Objective Function
profit = pulp.lpSum([
    (data['selling_price'] - data['material_cost']) * (regular_basket[w] + overtime_basket[w]) -
    data['regular_cost'] * regular_used[w] -
    data['overtime_cost'] * overtime_used[w] -
    data['holding_cost'] * inventory[w]
    for w in range(W)
])
profit += data['salvage_value'] * inventory[W-1]
problem += profit, "Total_Profit"

# Constraints
for w in range(W):
    # Labor Constraints
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w], f"Labor_Constraint_{w}"

    # Assembly Constraints
    problem += regular_basket[w] + overtime_basket[w] <= (regular_used[w] + overtime_used[w]) / data['assembly_time'], f"Assembly_Constraint_{w}"

    # Inventory Constraints
    if w == 0:
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - data['demand'][w], f"Inventory_Constraint_{w}"
    else:
        problem += inventory[w-1] + regular_basket[w] + overtime_basket[w] - data['demand'][w] == inventory[w], f"Inventory_Constraint_{w}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')