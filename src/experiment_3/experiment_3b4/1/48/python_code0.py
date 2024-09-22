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

# Create a LP maximization problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Decision variables
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Continuous') for w in range(W)]
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, cat='Continuous') for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, cat='Continuous') for w in range(W)]

# Objective function
total_profit = (
    pulp.lpSum([
        data['selling_price'] * (regular_basket[w] + overtime_basket[w])
        - data['regular_cost'] * regular_used[w]
        - data['overtime_cost'] * overtime_used[w]
        - data['material_cost'] * (regular_basket[w] + overtime_basket[w])
        - data['holding_cost'] * inventory[w]
        for w in range(W)
    ]) + data['salvage_value'] * inventory[W-1]
)
problem += total_profit

# Constraints
# 1. Labor constraints
for w in range(W):
    problem += data['assembly_time'] * regular_basket[w] == regular_used[w]
    problem += data['assembly_time'] * overtime_basket[w] == overtime_used[w]

# 2. Demand and inventory balance
problem += inventory[0] == 0
for w in range(W):
    if w == 0:
        prev_inventory = 0  # For week 1
    else:
        prev_inventory = inventory[w-1]
    problem += regular_basket[w] + overtime_basket[w] + prev_inventory == data['demand'][w] + inventory[w]

# 3. Labor availability constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')