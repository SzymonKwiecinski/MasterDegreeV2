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

W = len(data['demand'])

# Problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(W), lowBound=0, cat='Continuous')
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(W), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(W + 1), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([
    data['selling_price'] * (regular_basket[w] + overtime_basket[w] - (inventory[w] if w < W else 0)) -
    data['regular_cost'] * regular_used[w] -
    data['overtime_cost'] * overtime_used[w] -
    (data['holding_cost'] * inventory[w] if w < W-1 else 0) +
    (data['salvage_value'] * inventory[w] if w == W else 0)
    for w in range(W)
])
problem += profit, "Total Profit"

# Constraints
problem += inventory[0] == 0, "Initial Inventory"

for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w], f"Regular Labor Limit_{w}"
    problem += overtime_used[w] <= data['overtime_labor'][w], f"Overtime Labor Limit_{w}"
    problem += regular_basket[w] == regular_used[w] * (1 / data['assembly_time']), f"Regular Basket Production_{w}"
    problem += overtime_basket[w] == overtime_used[w] * (1 / data['assembly_time']), f"Overtime Basket Production_{w}"
    problem += (regular_basket[w] + overtime_basket[w] +
                (inventory[w-1] if w > 0 else 0) - inventory[w]) == data['demand'][w], f"Demand Satisfaction_{w}"

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')