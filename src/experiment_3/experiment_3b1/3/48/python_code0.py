import pulp
import json

data = json.loads("""{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}""")

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
regular_basket = pulp.LpVariable.dicts("regular_basket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("overtime_basket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(W), lowBound=0)

# Initialize Problem
problem = pulp.LpProblem("Fine_Foods_Gift_Baskets", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum([
    (selling_price - material_cost) * (regular_basket[w] + overtime_basket[w]) -
    regular_cost * regular_used[w] -
    overtime_cost * overtime_used[w] -
    holding_cost * inventory[w]
    for w in range(W)
])
profit += salvage_value * inventory[W-1]

problem += profit

# Constraints
# Labor Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w]

# Demand Constraints
for w in range(W):
    inventory_prev = inventory[w-1] if w > 0 else 0
    problem += regular_basket[w] + overtime_basket[w] + inventory_prev == demand[w] + inventory[w]

# Assembly Time Constraints
for w in range(W):
    problem += regular_basket[w] * assembly_time <= regular_used[w]
    problem += overtime_basket[w] * assembly_time <= overtime_used[w]

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')