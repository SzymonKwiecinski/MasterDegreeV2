import pulp
import json

# Input data in JSON format
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

# Problem parameters
W = len(data['demand'])  # Number of weeks
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0, cat='Continuous')
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(W), lowBound=0, cat='Integer')
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(selling_price * (regular_baskets[w] + overtime_baskets[w]) 
                    - (regular_used[w] * regular_cost + overtime_used[w] * overtime_cost) 
                    - holding_cost * inventory[w] for w in range(W))
profit += pulp.lpSum(salvage_value * inventory[W-1])  # salvage value for week W
problem += profit

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w]
    
    # Production constraints
    problem += regular_baskets[w] * assembly_time <= regular_used[w]
    problem += overtime_baskets[w] * assembly_time <= overtime_used[w]

    # Demand constraints
    if w < W - 1:
        problem += regular_baskets[w] + overtime_baskets[w] + (inventory[w-1] if w > 0 else 0) - inventory[w] >= demand[w]
    else:
        problem += regular_baskets[w] + overtime_baskets[w] + (inventory[w-1] if w > 0 else 0) >= demand[w]

    # Inventory balance
    if w > 0:
        problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - demand[w]
    else:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - demand[w]

# Solve the problem
problem.solve()

# Output results
output = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(W)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(W)],
    "regular_baskets": [pulp.value(regular_baskets[w]) for w in range(W)],
    "overtime_baskets": [pulp.value(overtime_baskets[w]) for w in range(W)],
    "inventory": [pulp.value(inventory[w]) for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')