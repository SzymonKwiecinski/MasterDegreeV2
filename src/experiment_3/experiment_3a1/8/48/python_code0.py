import pulp

# Data from the provided JSON format
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

# Define the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(1, W + 1)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(1, W + 1)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(1, W + 1)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(1, W + 1)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(1, W + 1)]

# Objective function
total_profit = pulp.lpSum(
    (
        data['selling_price'] * (regular_basket[w] + overtime_basket[w]) 
        - data['regular_cost'] * regular_used[w] 
        - data['overtime_cost'] * overtime_used[w] 
        - data['material_cost'] * (regular_basket[w] + overtime_basket[w]) 
        - data['holding_cost'] * inventory[w]
    ) for w in range(W)
) + (data['salvage_value'] * inventory[W - 1])
problem += total_profit

# Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w]

for w in range(W):
    problem += regular_basket[w] == regular_used[w] / data['assembly_time']
    problem += overtime_basket[w] == overtime_used[w] / data['assembly_time']

for w in range(1, W):
    problem += inventory[w] == inventory[w - 1] + regular_basket[w] + overtime_basket[w] - data['demand'][w]

# Initial inventory for week 1
problem += inventory[0] == 0

# Non-negativity constraints are already enforced by defining the variables with lowBound=0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')