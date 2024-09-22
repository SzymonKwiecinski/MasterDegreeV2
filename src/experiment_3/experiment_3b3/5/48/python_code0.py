import pulp

# Data
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
W = len(data['demand'])
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']

# Problem
problem = pulp.LpProblem("Gift_Baskets_Assembly", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

# Objective Function
total_profit = pulp.lpSum(
    (selling_price - material_cost) * (regular_basket[w] + overtime_basket[w]) -
    (regular_cost * regular_used[w] + overtime_cost * overtime_used[w]) -
    holding_cost * inventory[w] for w in range(W)
)
problem += total_profit

# Constraints
for w in range(W):
    # Demand satisfaction
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] >= demand[w]
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] >= demand[w]

    # Labor hour constraints
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]

    # Labor hour usage for basket assembly
    problem += regular_used[w] == assembly_time * regular_basket[w]
    problem += overtime_used[w] == assembly_time * overtime_basket[w]

    # Inventory calculation
    if w == 0:
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - demand[w]
    else:
        problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - demand[w]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')