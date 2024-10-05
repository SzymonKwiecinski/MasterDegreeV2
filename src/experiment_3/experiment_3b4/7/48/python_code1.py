import pulp

# Data from the JSON
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

# Sets
weeks = range(len(data['demand']))

# Decision Variables
regular_used = pulp.LpVariable.dicts('regular_used', weeks, lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts('overtime_used', weeks, lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts('regular_basket', weeks, lowBound=0, cat='Continuous')
overtime_basket = pulp.LpVariable.dicts('overtime_basket', weeks, lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts('inventory', weeks, lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = (
    pulp.lpSum(data['selling_price'] * (regular_basket[w] + overtime_basket[w]) for w in weeks) -
    pulp.lpSum(data['material_cost'] * (regular_basket[w] + overtime_basket[w]) for w in weeks) -
    pulp.lpSum(data['regular_cost'] * regular_used[w] + data['overtime_cost'] * overtime_used[w] for w in weeks) -
    pulp.lpSum(data['holding_cost'] * inventory[w] for w in weeks[:-1]) +
    data['salvage_value'] * inventory[weeks[-1]]
)

problem += profit

# Constraints
for w in weeks:
    problem += regular_used[w] <= data['regular_labor'][w], f"Regular_Labor_Constraint_week_{w}"
    problem += overtime_used[w] <= data['overtime_labor'][w], f"Overtime_Labor_Constraint_week_{w}"
    problem += regular_basket[w] == regular_used[w] * data['assembly_time'], f"Regular_Basket_Production_week_{w}"
    problem += overtime_basket[w] == overtime_used[w] * data['assembly_time'], f"Overtime_Basket_Production_week_{w}"

# Inventory Constraints
problem += inventory[0] == regular_basket[0] + overtime_basket[0] - data['demand'][0], "Inventory_Balance_Week_0"

for w in weeks[1:]:
    problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - data['demand'][w], f"Inventory_Balance_week_{w}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')