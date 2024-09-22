import pulp

# Data from the input
data = {
    'regular_cost': 30,
    'overtime_cost': 45,
    'assembly_time': 0.4,
    'material_cost': 25,
    'selling_price': 65,
    'holding_cost': 4,
    'salvage_value': 30,
    'demand': [700, 1500, 2800, 1800],
    'regular_labor': [450, 550, 600, 600],
    'overtime_labor': [40, 200, 320, 160]
}

# Extract data points
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

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=regular_labor[w], cat='Continuous') for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=overtime_labor[w], cat='Continuous') for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(W)]

# Objective function: Maximize profit
profit_terms = [
    (selling_price * (regular_basket[w] + overtime_basket[w]) - 
     material_cost * (regular_basket[w] + overtime_basket[w]) - 
     regular_cost * regular_used[w] - 
     overtime_cost * overtime_used[w] - 
     holding_cost * (inventory[w] if w < W-1 else 0))
    for w in range(W)
]
salvage_terms = salvage_value * inventory[-1]
problem += pulp.lpSum(profit_terms) + salvage_terms

# Constraints
for w in range(W):
    problem += regular_used[w] == assembly_time * regular_basket[w], f"Regular_Labor_Usage_Week_{w}"
    problem += overtime_used[w] == assembly_time * overtime_basket[w], f"Overtime_Labor_Usage_Week_{w}"
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] == demand[w] + inventory[w], f"Demand_Fulfillment_Week_{w}"
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] == demand[w] + inventory[w], f"Demand_Fulfillment_Week_{w}"

# Solve the problem
problem.solve()

# Output the results
output = {
    "regular_used": [regular_used[w].varValue for w in range(W)],
    "overtime_used": [overtime_used[w].varValue for w in range(W)],
    "regular_baskets": [regular_basket[w].varValue for w in range(W)],
    "overtime_baskets": [overtime_basket[w].varValue for w in range(W)],
    "inventory": [inventory[w].varValue for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')