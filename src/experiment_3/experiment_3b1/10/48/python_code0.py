import pulp
import json

# Data
data_json = '''{
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
}'''

data = json.loads(data_json)

# Parameters
W = len(data['demand'])
demand = data['demand']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']

# Create a linear programming problem
problem = pulp.LpProblem("GiftBasketProduction", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

# Objective Function
total_profit = pulp.lpSum(
    (selling_price * (regular_basket[w] + overtime_basket[w]) 
     - (regular_cost * regular_used[w]) 
     - (overtime_cost * overtime_used[w]) 
     - (material_cost * (regular_basket[w] + overtime_basket[w])) 
     - (holding_cost * inventory[w])
    ) for w in range(W)
)

total_profit += salvage_value * inventory[W-1]  # Add salvage value for last week

problem += total_profit

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]
    
    # Production constraints
    problem += regular_basket[w] + overtime_basket[w] <= (regular_used[w] + overtime_used[w]) / assembly_time

# Inventory balance constraints
problem += inventory[0] == (regular_basket[0] + overtime_basket[0] - demand[0])
for w in range(1, W):
    problem += inventory[w] == (inventory[w-1] + regular_basket[w] + overtime_basket[w] - demand[w])

# Inventory non-negativity for the last week
problem += inventory[W-1] >= 0

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')