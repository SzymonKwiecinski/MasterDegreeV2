import pulp
import json

# Load data
data_json = '{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}'
data = json.loads(data_json)

# Problem parameters
W = len(data['demand'])
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

# Objective Function
profit_expr = pulp.lpSum(
    selling_price * (regular_basket[w] + overtime_basket[w]) -
    regular_cost * regular_used[w] -
    overtime_cost * overtime_used[w] -
    material_cost * (regular_basket[w] + overtime_basket[w]) -
    holding_cost * inventory[w]
    for w in range(W)
) + salvage_value * inventory[W-1]

problem += profit_expr

# Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] >= assembly_time * (regular_basket[w] + overtime_basket[w])
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]
    if w > 0:
        problem += inventory[w-1] + regular_basket[w] + overtime_basket[w] == data['demand'][w] + inventory[w]

# Initial inventory constraint
problem += inventory[0] == 0

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')