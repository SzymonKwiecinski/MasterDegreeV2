import pulp

# Data provided in the problem
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

# Constants
W = len(data['demand'])  # Number of weeks

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w+1}', lowBound=0, upBound=data['regular_labor'][w]) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w+1}', lowBound=0, upBound=data['overtime_labor'][w]) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w+1}', lowBound=0) for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w+1}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w+1}', lowBound=0) for w in range(W)]

# Objective function
profit = pulp.lpSum([
    data['selling_price'] * (regular_baskets[w] + overtime_baskets[w])
    - data['material_cost'] * (regular_baskets[w] + overtime_baskets[w])
    - data['regular_cost'] * regular_used[w]
    - data['overtime_cost'] * overtime_used[w]
    - data['holding_cost'] * inventory[w]
    for w in range(W)
]) + data['salvage_value'] * inventory[W-1]

problem += profit

# Constraints
for w in range(W):
    # Regular and overtime labor constraints
    problem += regular_baskets[w] == regular_used[w] / data['assembly_time']
    problem += overtime_baskets[w] == overtime_used[w] / data['assembly_time']

    # Demand and inventory constraints
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] - inventory[w] == data['demand'][w]
    else:
        problem += regular_baskets[w] + overtime_baskets[w] + inventory[w-1] - inventory[w] == data['demand'][w]

# Solve the problem
problem.solve()

# Prepare results
results = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

# Output results
print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')