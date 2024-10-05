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

# Parameters
W = len(data['demand'])

# Problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(W), lowBound=0, cat='Continuous')
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(W), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0, cat='Continuous')

# Objective Function
total_profit = pulp.lpSum([
    (regular_basket[w] + overtime_basket[w]) * data['selling_price'] -
    (regular_used[w] * data['regular_cost'] + overtime_used[w] * data['overtime_cost'] +
     regular_basket[w] * data['material_cost'] + inventory[w] * data['holding_cost'])
    for w in range(W)
]) + inventory[W-1] * data['salvage_value']

problem += total_profit

# Constraints
for w in range(W):
    # Regular labor constraint
    problem += regular_used[w] <= data['regular_labor'][w], f"Regular_Labor_Constraint_Week_{w+1}"
    
    # Overtime labor constraint
    problem += overtime_used[w] <= data['overtime_labor'][w], f"Overtime_Labor_Constraint_Week_{w+1}"
    
    # Labor availability
    problem += regular_used[w] + overtime_used[w] >= (regular_basket[w] + overtime_basket[w]) * data['assembly_time'], f"Labor_Availability_Week_{w+1}"
    
    # Inventory balance
    if w == 0:
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - data['demand'][w], f"Inventory_Balance_Week_{w+1}"
    else:
        problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - data['demand'][w], f"Inventory_Balance_Week_{w+1}"

# Ensure non-negative inventory at the end of the season
problem += inventory[W-1] >= 0, "Non_Negativity_End_Inventory"

# Solve the Problem
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')