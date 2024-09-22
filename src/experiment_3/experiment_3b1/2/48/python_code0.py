import pulp
import json

# Data input
data = json.loads("{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}")

# Parameters
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

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(W), lowBound=0, cat='Integer')
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum([
    (selling_price * (regular_baskets[w] + overtime_baskets[w]) - material_cost * (regular_baskets[w] + overtime_baskets[w]) -
     regular_cost * regular_used[w] - overtime_cost * overtime_used[w] - holding_cost * inventory[w])
    for w in range(W)
]) + pulp.lpSum([salvage_value * inventory[W - 1]])

problem += profit

# Constraints
# Labor availability
for w in range(W):
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]

# Labor requirement for baskets
for w in range(W):
    problem += regular_baskets[w] == regular_used[w] / assembly_time
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time

# Meeting demand
for w in range(W):
    inventory_prev = inventory[w - 1] if w > 0 else 0
    problem += regular_baskets[w] + overtime_baskets[w] + inventory_prev >= demand[w]

# Inventory flow
for w in range(W):
    inventory_prev = inventory[w - 1] if w > 0 else 0
    problem += inventory[w] == inventory_prev + regular_baskets[w] + overtime_baskets[w] - demand[w]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')