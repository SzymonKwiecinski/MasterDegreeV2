import pulp
import json

# Data input
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

# Extract data
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

# Number of weeks
W = len(demand)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
regular_used = pulp.LpVariable.dicts("regular_used", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("overtime_used", range(W), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("regular_baskets", range(W), lowBound=0)
overtime_baskets = pulp.LpVariable.dicts("overtime_baskets", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(W), lowBound=0)

# Objective function
profit = pulp.lpSum([selling_price * (regular_baskets[w] + overtime_baskets[w]) for w in range(W)]) \
         + salvage_value * inventory[W-1] \
         - pulp.lpSum([regular_cost * regular_used[w] + overtime_cost * overtime_used[w] for w in range(W)]) \
         - pulp.lpSum([material_cost * (regular_baskets[w] + overtime_baskets[w]) for w in range(W)]) \
         - pulp.lpSum([holding_cost * inventory[w] for w in range(W-1)])

problem += profit

# Constraints
# regular_baskets and overtime_baskets constraints
for w in range(W):
    problem += regular_baskets[w] == regular_used[w] / assembly_time
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time

# Inventory constraints
problem += inventory[0] == 0
for w in range(1, W):
    problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - demand[w]

# Labor constraints
for w in range(W):
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')