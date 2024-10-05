import pulp

# Data from the problem
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

# Extract information from data
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

# Define the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=regular_labor[w], cat='Continuous') for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=overtime_labor[w], cat='Continuous') for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Continuous') for w in range(W)]

# Objective function (maximize profit)
total_revenue = pulp.lpSum(selling_price * (regular_basket[w] + overtime_basket[w]) for w in range(W))
total_cost_regular = pulp.lpSum(regular_cost * regular_used[w] for w in range(W))
total_cost_overtime = pulp.lpSum(overtime_cost * overtime_used[w] for w in range(W))
total_cost_material = pulp.lpSum(material_cost * (regular_basket[w] + overtime_basket[w]) for w in range(W))
total_holding_cost = pulp.lpSum(holding_cost * inventory[w] for w in range(W - 1))
salvage_value_revenue = salvage_value * inventory[W - 1]

problem += total_revenue + salvage_value_revenue - (total_cost_regular + total_cost_overtime + total_cost_material + total_holding_cost)

# Constraints
for w in range(W):
    problem += regular_basket[w] == regular_used[w] / assembly_time
    problem += overtime_basket[w] == overtime_used[w] / assembly_time
    
    # Demand constraints
    production = regular_basket[w] + overtime_basket[w]
    if w == 0:
        problem += production == demand[w] + inventory[w]
    else:
        problem += production + inventory[w - 1] == demand[w] + inventory[w]

# Solve the problem
problem.solve()

# Gather results
results = {
    "regular_used": [regular_used[w].varValue for w in range(W)],
    "overtime_used": [overtime_used[w].varValue for w in range(W)],
    "regular_baskets": [regular_basket[w].varValue for w in range(W)],
    "overtime_baskets": [overtime_basket[w].varValue for w in range(W)],
    "inventory": [inventory[w].varValue for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')