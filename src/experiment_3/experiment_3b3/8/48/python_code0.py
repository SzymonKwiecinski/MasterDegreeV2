import pulp

# Data from JSON
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
W = len(data['demand'])

# Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_baskets_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_baskets_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(W)]

# Objective Function
total_profit = (
    pulp.lpSum(
        (regular_baskets[w] + overtime_baskets[w]) * data['selling_price']
        - (regular_used[w] * data['regular_cost'] + overtime_used[w] * data['overtime_cost'])
        - (regular_baskets[w] + overtime_baskets[w]) * data['material_cost']
        - inventory[w] * data['holding_cost']
        for w in range(W)
    ) + inventory[W-1] * data['salvage_value']
)
problem += total_profit

# Constraints

# 1. Labor constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w]
    problem += regular_baskets[w] * data['assembly_time'] <= regular_used[w]
    problem += overtime_baskets[w] * data['assembly_time'] <= overtime_used[w]

# 2. Demand fulfillment
for w in range(W):
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] >= data['demand'][w]
        continue
    problem += regular_baskets[w] + overtime_baskets[w] + inventory[w-1] >= data['demand'][w]
    problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w]

# 3. Initial inventory
problem += inventory[0] == regular_baskets[0] + overtime_baskets[0] - data['demand'][0]

# Solve the problem
problem.solve()

# Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')