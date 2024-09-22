import pulp
import json

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
W = len(data['demand'])
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

# Objective Function
profit = pulp.lpSum([
    data['selling_price'] * (regular_baskets[w] + overtime_baskets[w]) -
    (data['regular_cost'] * regular_used[w] + data['overtime_cost'] * overtime_used[w]) -
    data['material_cost'] * (regular_baskets[w] + overtime_baskets[w]) -
    (data['holding_cost'] * inventory[w] if w < W-1 else 0)
    for w in range(W)
])
profit += pulp.lpSum(
    (data['salvage_value'] * inventory[W-1]) if W-1 == w else 0 for w in range(W)
)
problem += profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]
    
    # Labor constraints
    problem += regular_used[w] / data['assembly_time'] + overtime_used[w] / data['assembly_time'] >= data['demand'][w]
    
    # Inventory balance
    if w == 0:
        problem += inventory[w] == (regular_baskets[w] + overtime_baskets[w] - data['demand'][w])
    else:
        problem += inventory[w] == (inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w])

# Solve the problem
problem.solve()

# Output results
result = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{result["total_profit"]}</OBJ>')