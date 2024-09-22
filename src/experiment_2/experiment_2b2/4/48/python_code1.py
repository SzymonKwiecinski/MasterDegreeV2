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

# Parameters
W = len(data['demand'])
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']

# Decision Variables
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(W+1), lowBound=0, cat='Continuous')

regular_baskets = pulp.LpVariable.dicts("Regular_Baskets", range(W), lowBound=0, cat='Continuous')
overtime_baskets = pulp.LpVariable.dicts("Overtime_Baskets", range(W), lowBound=0, cat='Continuous')

# Constraints
problem += inventory[0] == 0, "Initial_Inventory"
for w in range(W):
    problem += regular_used[w] <= regular_labor[w], f"Regular_Labor_Constraint_{w}"
    problem += overtime_used[w] <= overtime_labor[w], f"Overtime_Labor_Constraint_{w}"
    
    problem += regular_baskets[w] == regular_used[w] * (1 / assembly_time), f"Regular_Baskets_Produced_{w}"
    problem += overtime_baskets[w] == overtime_used[w] * (1 / assembly_time), f"Overtime_Baskets_Produced_{w}"
    
    problem += regular_baskets[w] + overtime_baskets[w] + inventory[w] >= demand[w] + inventory[w+1], f"Demand_Satisfaction_{w}"

# Objective function
total_revenue = pulp.lpSum(selling_price * (regular_baskets[w] + overtime_baskets[w]) for w in range(W))
total_regular_cost = pulp.lpSum(regular_cost * regular_used[w] for w in range(W))
total_overtime_cost = pulp.lpSum(overtime_cost * overtime_used[w] for w in range(W))
total_material_cost = pulp.lpSum(material_cost * (regular_baskets[w] + overtime_baskets[w]) for w in range(W))
total_holding_cost = pulp.lpSum(holding_cost * inventory[w] for w in range(W))
salvaged_value = salvage_value * inventory[W]

profit = total_revenue - total_regular_cost - total_overtime_cost - total_material_cost - total_holding_cost + salvaged_value
problem += profit

# Solve the problem
problem.solve()

# Extract results
results = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w+1]) for w in range(W)],
    "total_profit": pulp.value(profit)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')