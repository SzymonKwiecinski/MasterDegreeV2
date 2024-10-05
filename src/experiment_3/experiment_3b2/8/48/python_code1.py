import pulp
import json

# Data in JSON format
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

# Decision Variables
W = len(data['demand'])
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W + 1), lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
total_profit = pulp.lpSum([
    (data['selling_price'] * (regular_basket[w] + overtime_basket[w])) - 
    (data['material_cost'] * (regular_basket[w] + overtime_basket[w])) - 
    (data['holding_cost'] * inventory[w-1]) 
    for w in range(1, W + 1)
]) + (data['salvage_value'] * inventory[W])

problem += total_profit

# Labor Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w], f"Regular_Labor_Constraint_{w}"
    problem += overtime_used[w] <= data['overtime_labor'][w], f"Overtime_Labor_Constraint_{w}"

# Basket Assembly
for w in range(W):
    problem += regular_basket[w] == regular_used[w] / data['assembly_time'], f"Regular_Basket_Assembly_{w}"
    problem += overtime_basket[w] == overtime_used[w] / data['assembly_time'], f"Overtime_Basket_Assembly_{w}"

# Inventory Balance
problem += inventory[0] == 0, "Initial_Inventory"

for w in range(1, W + 1):
    problem += inventory[w] == inventory[w-1] + regular_basket[w-1] + overtime_basket[w-1] - data['demand'][w-1], f"Inventory_Balance_{w}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')