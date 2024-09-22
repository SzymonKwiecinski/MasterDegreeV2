import pulp
import json

# Given data in JSON format
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

# Parameters
W = len(data['demand'])  # number of weeks
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

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(1, W + 1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(1, W + 1), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(1, W + 1), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(1, W + 1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(1, W + 1), lowBound=0)

# Problem definition
problem = pulp.LpProblem("GiftBasketProduction", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum((selling_price - material_cost) * (regular_basket[w] + overtime_basket[w]) for w in range(1, W + 1))
costs = pulp.lpSum(regular_used[w] * regular_cost + overtime_used[w] * overtime_cost for w in range(1, W + 1))
holding_costs = pulp.lpSum(holding_cost * inventory[w] for w in range(1, W)) - salvage_value * inventory[W]
problem += profit - costs - holding_costs, "Total_Profit"

# Constraints
# Labor hours constraint
for w in range(1, W + 1):
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w - 1] + overtime_labor[w - 1], f"LaborConstraint_{w}"

# Baskets production constraint
for w in range(1, W + 1):
    problem += regular_basket[w] == regular_used[w] / assembly_time, f"RegularProductionConstraint_{w}"
    problem += overtime_basket[w] == overtime_used[w] / assembly_time, f"OvertimeProductionConstraint_{w}"

# Inventory balance constraint
problem += inventory[1] == regular_basket[1] + overtime_basket[1] - demand[0], "InventoryBalance_Week1"
for w in range(2, W + 1):
    problem += inventory[w] == inventory[w - 1] + regular_basket[w] + overtime_basket[w] - demand[w - 1], f"InventoryBalance_Week_{w}"
problem += inventory[W] >= 0, "NonNegInventory_WeekW"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')