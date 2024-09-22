import pulp
import json

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

W = len(data['demand'])  # Total number of weeks

# Define the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

# Objective Function
profit = pulp.lpSum([
    (data['selling_price'] * (regular_basket[w] + overtime_basket[w])) -
    (data['material_cost'] * (regular_basket[w] + overtime_basket[w])) -
    (data['regular_cost'] * regular_used[w]) -
    (data['overtime_cost'] * overtime_used[w]) -
    (data['holding_cost'] * inventory[w])
    for w in range(W)
]) + (data['salvage_value'] * inventory[W-1])

problem += profit

# Constraints

# Labor constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w], f"RegularLaborConstraint_{w}"
    problem += overtime_used[w] <= data['overtime_labor'][w], f"OvertimeLaborConstraint_{w}"

# Production constraints
for w in range(W):
    problem += regular_basket[w] == regular_used[w] / data['assembly_time'], f"RegularProductionConstraint_{w}"
    problem += overtime_basket[w] == overtime_used[w] / data['assembly_time'], f"OvertimeProductionConstraint_{w}"

# Demand fulfillment and inventory constraints
problem += inventory[0] == 0, "InitialInventoryConstraint"
for w in range(1, W):
    problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - data['demand'][w], f"InventoryConstraint_{w}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')