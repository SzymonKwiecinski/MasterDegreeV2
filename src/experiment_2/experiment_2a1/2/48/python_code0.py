import json
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

# Parameters
W = len(data['demand'])  # Number of weeks
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
assembly_time = data['assembly_time']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

# Create the LP problem
problem = pulp.LpProblem("GiftBasketProduction", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

# Objective function
total_profit = pulp.lpSum([
    (selling_price - material_cost) * (regular_baskets[w] + overtime_baskets[w]) - \
    (regular_used[w] * regular_cost + overtime_used[w] * overtime_cost) - \
    holding_cost * inventory[w] for w in range(W)
]) + salvage_value * inventory[W-1]

problem += total_profit

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w]
    # Baskets assembly constraints
    problem += regular_baskets[w] + overtime_baskets[w] <= (regular_used[w] / assembly_time) + \
                        (overtime_used[w] / assembly_time)
    # Demand satisfaction and inventory constraints
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] >= demand[w]
        problem += inventory[w] == (regular_baskets[w] + overtime_baskets[w] - demand[w])
    else:
        problem += inventory[w-1] + regular_baskets[w] + overtime_baskets[w] >= demand[w]
        problem += inventory[w] == (inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - demand[w])

# Solve the problem
problem.solve()

# Collecting results
results = {
    "regular_used": [pulp.value(v) for v in regular_used],
    "overtime_used": [pulp.value(v) for v in overtime_used],
    "regular_baskets": [pulp.value(v) for v in regular_baskets],
    "overtime_baskets": [pulp.value(v) for v in overtime_baskets],
    "inventory": [pulp.value(v) for v in inventory],
    "total_profit": pulp.value(problem.objective)
}

# Output results
print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')