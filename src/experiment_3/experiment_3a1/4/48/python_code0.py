import pulp
import json

# Data provided in JSON format
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

# Assigning parameters from data
W = len(data['demand'])
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

# Initialize the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(1, W + 1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(1, W + 1), lowBound=0)
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(1, W + 1), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(1, W + 1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(1, W + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum([
    selling_price * (regular_basket[w] + overtime_basket[w]) 
    - regular_cost * regular_used[w] 
    - overtime_cost * overtime_used[w] 
    - material_cost * (regular_basket[w] + overtime_basket[w]) 
    - holding_cost * inventory[w] 
    for w in range(1, W + 1)
]) + salvage_value * inventory[W], "Total_Profit"

# Constraints
for w in range(1, W + 1):
    problem += regular_used[w] <= regular_labor[w - 1], f"Regular_Labor_Constraint_{w}"
    problem += overtime_used[w] <= overtime_labor[w - 1], f"Overtime_Labor_Constraint_{w}"
    problem += regular_used[w] + overtime_used[w] >= assembly_time * (regular_basket[w] + overtime_basket[w]), f"Assembly_Time_Constraint_{w}"

for w in range(2, W + 1):
    problem += regular_basket[w] + overtime_basket[w] + inventory[w - 1] == demand[w - 1] + inventory[w], f"Demand_Constraint_{w}"

problem += inventory[1] == 0, "Initial_Inventory"
problem += inventory[W] >= 0, "Final_Inventory_Salvage"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')