import pulp
import json

# Data
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

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
regular_used = pulp.LpVariable.dicts("regular_used", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("overtime_used", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("regular_basket", range(W), lowBound=0, cat='Integer')
overtime_basket = pulp.LpVariable.dicts("overtime_basket", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("inventory", range(W + 1), lowBound=0, cat='Integer')

# Problem Definition
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum([
    (selling_price * (regular_basket[w] + overtime_basket[w]) 
     - regular_cost * regular_used[w] 
     - overtime_cost * overtime_used[w] 
     - material_cost * (regular_basket[w] + overtime_basket[w]) 
     - holding_cost * inventory[w])
    for w in range(W)
]) + salvage_value * inventory[W]

problem += profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]
    problem += regular_basket[w] == regular_used[w] / assembly_time
    problem += overtime_basket[w] == overtime_used[w] / assembly_time
    problem += demand[w] + (inventory[w - 1] if w > 0 else 0) == regular_basket[w] + overtime_basket[w] + inventory[w]

# Initial inventory
problem += inventory[0] == 0

# Solve the problem
problem.solve()

# Output result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')