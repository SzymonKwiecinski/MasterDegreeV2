import pulp
import json

data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}

# Problem setup
W = len(data['demand'])
problem = pulp.LpProblem("Basket_Production", pulp.LpMaximize)

# Decision variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), 0, None)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), 0, None)
regular_baskets = pulp.LpVariable.dicts("Regular_Baskets", range(W), 0, None, pulp.LpInteger)
overtime_baskets = pulp.LpVariable.dicts("Overtime_Baskets", range(W), 0, None, pulp.LpInteger)
inventory = pulp.LpVariable.dicts("Inventory", range(W), 0, None)

# Objective function
profit = pulp.lpSum((data['selling_price'] - data['material_cost']) * (regular_baskets[w] + overtime_baskets[w]) for w in range(W))
cost_regular = pulp.lpSum(data['regular_cost'] * regular_used[w] for w in range(W))
cost_overtime = pulp.lpSum(data['overtime_cost'] * overtime_used[w] for w in range(W))
holding_costs = pulp.lpSum(data['holding_cost'] * inventory[w] for w in range(W - 1))  # No holding cost in last week
salvage_value = inventory[W - 1] * data['salvage_value']  # Only salvage on last week's inventory

problem += profit - cost_regular - cost_overtime - holding_costs + salvage_value

# Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w]
    problem += regular_baskets[w] == regular_used[w] / data['assembly_time']
    problem += overtime_baskets[w] == overtime_used[w] / data['assembly_time']
    
    if w == 0:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - data['demand'][w]
    else:
        problem += inventory[w] == inventory[w - 1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w]

# Solve the problem
problem.solve()

# Output results
output = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')