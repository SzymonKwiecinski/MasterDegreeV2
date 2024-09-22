import pulp
import json

# Data input
data = json.loads("{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}")

# Parameters
W = len(data['demand'])
demand = data['demand']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(W), lowBound=0, cat='Integer')
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

# Objective Function
profit = pulp.lpSum([
    (regular_basket[w] + overtime_basket[w]) * selling_price -
    (regular_used[w] * regular_cost + overtime_used[w] * overtime_cost + regular_basket[w] * material_cost) -
    holding_cost * inventory[w]
    for w in range(W)
]) + (salvage_value * inventory[W-1])

problem += profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]
    problem += regular_used[w] + overtime_used[w] >= assembly_time * (regular_basket[w] + overtime_basket[w])
    if w == 0:
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - demand[w]
    else:
        problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - demand[w]
    
problem += inventory[W-1] >= 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')