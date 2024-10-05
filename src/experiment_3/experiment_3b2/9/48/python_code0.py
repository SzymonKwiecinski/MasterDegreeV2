import pulp
import json

data = json.loads("{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}")

# Extracting data from JSON
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
W = len(demand)

# Problem definition
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("regular_used", range(1, W+1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("overtime_used", range(1, W+1), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("regular_baskets", range(1, W+1), lowBound=0)
overtime_baskets = pulp.LpVariable.dicts("overtime_baskets", range(1, W+1), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(0, W+1), lowBound=0)

# Objective Function
profit = pulp.lpSum([(selling_price * (regular_baskets[w] + overtime_baskets[w]) 
                      - regular_cost * regular_used[w] 
                      - overtime_cost * overtime_used[w] 
                      - material_cost * (regular_baskets[w] + overtime_baskets[w]) 
                      - holding_cost * inventory[w-1]) for w in range(1, W+1)]) + salvage_value * inventory[W]
problem += profit

# Constraints
# Regular Labor Constraint
for w in range(1, W+1):
    problem += regular_used[w] <= regular_labor[w-1]

# Overtime Labor Constraint
for w in range(1, W+1):
    problem += overtime_used[w] <= overtime_labor[w-1]

# Assembly Time Constraint
for w in range(1, W+1):
    problem += regular_baskets[w] == regular_used[w] / assembly_time
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time

# Demand Constraint
for w in range(1, W+1):
    problem += inventory[w-1] + regular_baskets[w] + overtime_baskets[w] == demand[w-1] + inventory[w]

# Initial Inventory Constraint
problem += inventory[0] == 0

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')