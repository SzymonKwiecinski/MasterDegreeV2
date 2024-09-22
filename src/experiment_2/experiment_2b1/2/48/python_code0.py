import pulp
import json

data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}

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
W = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(W), lowBound=0, cat='Integer')
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

# Objective function
total_profit = pulp.lpSum((selling_price * (regular_baskets[w] + overtime_baskets[w])) - 
                           (material_cost * (regular_baskets[w] + overtime_baskets[w])) - 
                           (regular_used[w] * regular_cost) - 
                           (overtime_used[w] * overtime_cost) - 
                           (holding_cost * inventory[w]) for w in range(W))

problem += total_profit + pulp.lpSum(salvage_value * inventory[W-1])  # Salvage value for the last week

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w]
    
    # Basket production constraints
    problem += regular_baskets[w] == regular_used[w] / assembly_time
    problem += overtime_baskets[w] == overtime_used[w] / assembly_time
    
    # Demand and inventory constraints
    if w == 0:
        problem += (regular_baskets[w] + overtime_baskets[w]) == demand[w] + inventory[w]
    else:
        problem += (regular_baskets[w] + overtime_baskets[w] + inventory[w-1]) == demand[w] + inventory[w]
    
    # Inventory is bounded by the holding cost
    problem += inventory[w] >= 0

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "regular_used": [regular_used[w].varValue for w in range(W)],
    "overtime_used": [overtime_used[w].varValue for w in range(W)],
    "regular_baskets": [regular_baskets[w].varValue for w in range(W)],
    "overtime_baskets": [overtime_baskets[w].varValue for w in range(W)],
    "inventory": [inventory[w].varValue for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

# Print the result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')