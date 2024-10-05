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

# Number of weeks
W = len(data['demand'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_baskets_{w}', lowBound=0) for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_baskets_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W+1)]

# Initial Inventory
inventory[0] = 0

# Objective Function
profit = pulp.lpSum([
    data['selling_price'] * (regular_baskets[w] + overtime_baskets[w]) 
    - data['material_cost'] * (regular_baskets[w] + overtime_baskets[w])
    - data['regular_cost'] * regular_used[w]
    - data['overtime_cost'] * overtime_used[w]
    - data['holding_cost'] * inventory[w]
    for w in range(W)
]) + data['salvage_value'] * inventory[W]

problem += profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]
    problem += regular_baskets[w] == regular_used[w] / data['assembly_time']
    problem += overtime_baskets[w] == overtime_used[w] / data['assembly_time']

    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] - data['demand'][w] == inventory[w+1]
    else:
        problem += (
            sum(regular_baskets[i] + overtime_baskets[i] for i in range(w+1)) 
            - sum(data['demand'][i] for i in range(w+1)) == inventory[w+1]
        )

problem += inventory[0] == 0
problem += inventory[W] >= 0

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')