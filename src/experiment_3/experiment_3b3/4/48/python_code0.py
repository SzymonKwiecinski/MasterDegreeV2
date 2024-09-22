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

# Create the problem
problem = pulp.LpProblem("Fine_Foods_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts('regular_used', range(W), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts('overtime_used', range(W), lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts('regular_basket', range(W), lowBound=0, cat='Continuous')
overtime_basket = pulp.LpVariable.dicts('overtime_basket', range(W), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts('inventory', range(W), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([
    data['selling_price'] * (regular_basket[w] + overtime_basket[w]) -
    (regular_used[w] * data['regular_cost'] + overtime_used[w] * data['overtime_cost'] +
     data['material_cost'] * (regular_basket[w] + overtime_basket[w])) -
    data['holding_cost'] * inventory[w]
    for w in range(W)
])

# Add salvage value for final week
problem += pulp.lpSum([
    -data['salvage_value'] * inventory[W-1]
])

# Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w], f"LaborLimitWeek{w}"
    problem += regular_basket[w] == regular_used[w] / data['assembly_time'], f"RegularBasketWeek{w}"
    problem += overtime_basket[w] == overtime_used[w] / data['assembly_time'], f"OvertimeBasketWeek{w}"

# Inventory constraints
problem += inventory[0] == regular_basket[0] + overtime_basket[0] - data['demand'][0], "InitialInventory"

for w in range(1, W):
    problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - data['demand'][w], f"InventoryBalanceWeek{w}"

# Solve
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')