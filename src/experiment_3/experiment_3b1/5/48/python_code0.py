import pulp
import json

data = json.loads("<DATA>{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>")

# Extracting data
W = len(data['demand'])
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

# Create the problem
problem = pulp.LpProblem("Fine_Foods_Profit_Maximization", pulp.LpMaximize)

# Decision variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W + 1), lowBound=0)

# Objective function
total_profit = pulp.lpSum([
    (selling_price * (regular_basket[w] + overtime_basket[w]) -
     (material_cost * (regular_basket[w] + overtime_basket[w])) -
     (regular_cost * regular_used[w]) -
     (overtime_cost * overtime_used[w]) -
     (holding_cost * inventory[w]))
    for w in range(W)
]) + (salvage_value * inventory[W])

problem += total_profit

# Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w], f"Labor_Constraint_{w}"
    problem += regular_basket[w] + overtime_basket[w] == (regular_used[w] + overtime_used[w]) / assembly_time, f"Assembly_Constraint_{w}"
    if w > 0:
        problem += inventory[w - 1] + regular_basket[w] + overtime_basket[w] - demand[w] == inventory[w], f"Inventory_Constraint_{w}"
    else:
        problem += inventory[0] == 0, "Initial_Inventory_Constraint"
    
problem += inventory[W] >= 0, "Final_Inventory_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')