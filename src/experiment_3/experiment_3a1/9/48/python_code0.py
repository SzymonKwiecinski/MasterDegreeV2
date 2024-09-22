import pulp
import json

# Data in JSON format
data_json = """
{
    "regular_cost": 30,
    "overtime_cost": 45,
    "assembly_time": 0.4,
    "material_cost": 25,
    "selling_price": 65,
    "holding_cost": 4,
    "salvage_value": 30,
    "demand": [700, 1500, 2800, 1800],
    "regular_labor": [450, 550, 600, 600],
    "overtime_labor": [40, 200, 320, 160]
}
"""
data = json.loads(data_json)

# Parameters
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

# Decision Variables
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]
total_profit = pulp.LpVariable('total_profit', lowBound=0)

# Objective Function
profit = pulp.lpSum([
    (selling_price * (regular_basket[w] + overtime_basket[w])) -
    (regular_cost * regular_used[w]) -
    (overtime_cost * overtime_used[w]) -
    (material_cost * (regular_basket[w] + overtime_basket[w])) -
    (holding_cost * inventory[w])
    for w in range(W)
])
problem += profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]
    problem += regular_basket[w] == regular_used[w] / assembly_time
    problem += overtime_basket[w] == overtime_used[w] / assembly_time

    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] >= demand[w]
    else:
        problem += (regular_basket[w] + overtime_basket[w] + inventory[w-1]) >= demand[w]

    problem += inventory[w] == (regular_basket[w] + overtime_basket[w] + (inventory[w-1] if w > 0 else 0)) - demand[w]

problem += inventory[W-1] >= 0
problem += total_profit == profit + salvage_value * inventory[W-1]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')