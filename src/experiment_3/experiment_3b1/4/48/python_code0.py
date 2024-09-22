import pulp
import json

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
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Fine_Foods_Company", pulp.LpMaximize)

# Objective Function
total_profit = pulp.lpSum([
    (selling_price * (regular_basket[w] + overtime_basket[w]) - 
     material_cost * (regular_basket[w] + overtime_basket[w])) for w in range(W)
]) - pulp.lpSum([holding_cost * inventory[w] for w in range(W)]) + \
salvage_value * inventory[W-1]

problem += total_profit

# Constraints
# Labor constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w]

# Basket assembly constraints
for w in range(W):
    problem += regular_basket[w] == regular_used[w] / assembly_time
    problem += overtime_basket[w] == overtime_used[w] / assembly_time

# Demand satisfaction constraints
for w in range(1, W):
    problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] >= demand[w]

# Inventory balance
problem += inventory[0] == 0  # inventory_1 = 0
for w in range(1, W):
    problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - demand[w]

# Final inventory constraint
problem += inventory[W-1] == pulp.lpSum(regular_basket[w] + overtime_basket[w] for w in range(W)) - pulp.lpSum(demand)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')