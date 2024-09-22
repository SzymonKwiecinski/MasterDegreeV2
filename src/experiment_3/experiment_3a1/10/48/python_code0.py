import pulp

# Data from the provided JSON
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

W = len(data['demand'])  # Number of weeks

# Create the problem
problem = pulp.LpProblem("Fine_Foods_Company_Optimization", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("Regular_Baskets", range(W), lowBound=0, cat='Integer')
overtime_baskets = pulp.LpVariable.dicts("Overtime_Baskets", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W + 1), lowBound=0)

# Objective Function
total_profit = pulp.lpSum(
    (data['selling_price'] * (regular_baskets[w] + overtime_baskets[w]) - 
     data['regular_cost'] * regular_used[w] - 
     data['overtime_cost'] * overtime_used[w] - 
     data['material_cost'] * (regular_baskets[w] + overtime_baskets[w]))
    for w in range(W)) - pulp.lpSum(data['holding_cost'] * inventory[w] for w in range(W - 1)) + data['salvage_value'] * inventory[W]
problem += total_profit, "Total_Profit"

# Constraints
for w in range(W):
    # Labor Constraints
    problem += regular_used[w] <= data['regular_labor'][w], f"Regular_Labor_Capacity_Week_{w}"
    problem += overtime_used[w] <= data['overtime_labor'][w], f"Overtime_Labor_Capacity_Week_{w}"
    problem += regular_used[w] == regular_baskets[w] * data['assembly_time'], f"Regular_Labor_Used_Week_{w}"
    problem += overtime_used[w] == overtime_baskets[w] * data['assembly_time'], f"Overtime_Labor_Used_Week_{w}"

    # Demand Satisfaction
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] >= data['demand'][w], f"Demand_Satisfaction_Week_{w}"
    else:
        problem += (regular_baskets[w] + overtime_baskets[w] + inventory[w - 1] >= data['demand'][w],
                     f"Demand_Satisfaction_Week_{w}")

    # Inventory Constraints
    if w == 0:
        problem += inventory[w] == (regular_baskets[w] + overtime_baskets[w] - data['demand'][w]), f"Inventory_Week_{w}"
    else:
        problem += inventory[w] == inventory[w - 1] + (regular_baskets[w] + overtime_baskets[w]) - data['demand'][w], f"Inventory_Week_{w}"

# Initial Inventory
problem += inventory[0] == 0, "Initial_Inventory"

# Ensuring non-negative inventory at the end of the last week
problem += inventory[W] >= 0, "Ending_Inventory_Non_Negative"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')