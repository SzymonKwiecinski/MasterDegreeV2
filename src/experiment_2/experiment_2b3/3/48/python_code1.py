import pulp

# Input Data
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

# Define the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Get the number of weeks
weeks = len(data['demand'])

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=data['regular_labor'][w], cat='Continuous') for w in range(weeks)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=data['overtime_labor'][w], cat='Continuous') for w in range(weeks)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Continuous') for w in range(weeks)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Continuous') for w in range(weeks)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Continuous') for w in range(weeks)]

# Objective Function: Maximize Profit
profit = pulp.lpSum([
    data['selling_price'] * (regular_basket[w] + overtime_basket[w]) -
    data['material_cost'] * (regular_basket[w] + overtime_basket[w]) -
    data['regular_cost'] * regular_used[w] -
    data['overtime_cost'] * overtime_used[w] -
    data['holding_cost'] * inventory[w]
    for w in range(weeks)
]) + data['salvage_value'] * inventory[-1]
problem += profit

# Constraints
for w in range(weeks):
    # Assembly constraints
    problem += (regular_basket[w] == regular_used[w] / data['assembly_time'])
    problem += (overtime_basket[w] == overtime_used[w] / data['assembly_time'])

    # Balance constraints
    if w == 0:
        problem += (regular_basket[w] + overtime_basket[w] == data['demand'][w] + inventory[w])
    else:
        problem += (regular_basket[w] + overtime_basket[w] + inventory[w-1] == data['demand'][w] + inventory[w])

# Solve the problem
problem.solve()

# Output Results
output = {
    "regular_used": [regular_used[w].varValue for w in range(weeks)],
    "overtime_used": [overtime_used[w].varValue for w in range(weeks)],
    "regular_baskets": [regular_basket[w].varValue for w in range(weeks)],
    "overtime_baskets": [overtime_basket[w].varValue for w in range(weeks)],
    "inventory": [inventory[w].varValue for w in range(weeks)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')