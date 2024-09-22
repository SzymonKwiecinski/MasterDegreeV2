import pulp
import json

# Data input
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

# Parameters
W = len(data['demand'])
demand = data['demand']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']

# Define the problem
problem = pulp.LpProblem("Basket_Assembly_Problem", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(1, W + 1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(1, W + 1), lowBound=0)
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(1, W + 1), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(1, W + 1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(1, W + 1), lowBound=0)

# Objective Function
profit_expressions = []
for w in range(1, W + 1):
    profit_expressions.append((selling_price - material_cost) * (regular_basket[w] + overtime_basket[w]) - regular_cost * regular_used[w] - overtime_cost * overtime_used[w] - holding_cost * inventory[w])
    
profit_expressions.append(salvage_value * inventory[W])  # salvage value for the last week
problem += pulp.lpSum(profit_expressions), "Total_Profit"

# Constraints
for w in range(1, W + 1):
    # Labor Constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w - 1] + overtime_labor[w - 1], f"Labor_Constraint_{w}"

    # Assembly Time Constraint
    problem += regular_basket[w] + overtime_basket[w] <= (regular_used[w] + overtime_used[w]) / assembly_time, f"Assembly_Time_Constraint_{w}"
    
    # Demand Satisfaction Constraints
    if w == 1:
        problem += regular_basket[w] + overtime_basket[w] == demand[w - 1] + inventory[w], f"Demand_Constraint_{w}"
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w - 1] == demand[w - 1] + inventory[w], f"Demand_Constraint_{w}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')