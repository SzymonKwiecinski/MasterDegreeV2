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

# Initialize the problem
W = len(data['demand'])
problem = pulp.LpProblem("Fine_Foods", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(1, W + 1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(1, W + 1), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(1, W + 1), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(1, W + 1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(1, W + 1), lowBound=0)

# Objective Function
revenue = pulp.lpSum((data['selling_price'] - data['material_cost']) * (regular_basket[w] + overtime_basket[w]) for w in range(1, W + 1))
costs = pulp.lpSum(data['regular_cost'] * regular_used[w] + data['overtime_cost'] * overtime_used[w] for w in range(1, W + 1))
holding_costs = pulp.lpSum(data['holding_cost'] * inventory[w] for w in range(1, W))
salvage_value = data['salvage_value'] * inventory[W]
problem += revenue - costs - holding_costs + salvage_value

# Constraints
for w in range(1, W + 1):
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w - 1] + data['overtime_labor'][w - 1]
    
for w in range(1, W + 1):
    problem += regular_basket[w] + overtime_basket[w] <= (regular_used[w] + overtime_used[w]) / data['assembly_time']
    
for w in range(1, W + 1):
    problem += regular_basket[w] + overtime_basket[w] + (inventory[w - 1] if w > 1 else 0) >= data['demand'][w - 1]
    
for w in range(2, W + 1):
    problem += inventory[w] == inventory[w - 1] + regular_basket[w] + overtime_basket[w] - data['demand'][w - 1]
    
problem += inventory[1] == 0  # Initial inventory

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')