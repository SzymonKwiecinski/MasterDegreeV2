import pulp

# Input data
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

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
weeks = len(data['demand'])

regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, upBound=data['regular_labor'][w], cat='Continuous') for w in range(weeks)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, upBound=data['overtime_labor'][w], cat='Continuous') for w in range(weeks)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Continuous') for w in range(weeks)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Continuous') for w in range(weeks)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Continuous') for w in range(weeks)]

# Add constraints
for w in range(weeks):
    problem += regular_used[w] * data['assembly_time'] == regular_basket[w]
    problem += overtime_used[w] * data['assembly_time'] == overtime_basket[w]
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] - inventory[w] == data['demand'][w]
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] - inventory[w] == data['demand'][w]

# Objective function
sales = pulp.lpSum(data['selling_price'] * (regular_basket[w] + overtime_basket[w]) for w in range(weeks))
regular_labor_cost = pulp.lpSum(data['regular_cost'] * regular_used[w] for w in range(weeks))
overtime_labor_cost = pulp.lpSum(data['overtime_cost'] * overtime_used[w] for w in range(weeks))
material_cost = pulp.lpSum(data['material_cost'] * (regular_basket[w] + overtime_basket[w]) for w in range(weeks))
holding_cost = pulp.lpSum(data['holding_cost'] * inventory[w] for w in range(weeks-1))
salvage_value = data['salvage_value'] * inventory[-1]

total_profit = sales - regular_labor_cost - overtime_labor_cost - material_cost - holding_cost + salvage_value
problem += total_profit

# Solve the problem
problem.solve()

# Output results
result = {
    "regular_used": [regular_used[w].varValue for w in range(weeks)],
    "overtime_used": [overtime_used[w].varValue for w in range(weeks)],
    "regular_baskets": [regular_basket[w].varValue for w in range(weeks)],
    "overtime_baskets": [overtime_basket[w].varValue for w in range(weeks)],
    "inventory": [inventory[w].varValue for w in range(weeks)],
    "total_profit": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')