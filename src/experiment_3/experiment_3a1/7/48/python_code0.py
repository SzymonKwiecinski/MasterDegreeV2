import pulp
import json

# Data provided in JSON format
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

# Create the LP problem
problem = pulp.LpProblem("GiftBasketProduction", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(1, W + 1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(1, W + 1), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(1, W + 1), lowBound=0)
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(1, W + 1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(1, W + 1), lowBound=0)

# Objective Function
profit = pulp.lpSum([(selling_price * (regular_baskets[w] + overtime_baskets[w])) -
                     (regular_cost * regular_used[w]) -
                     (overtime_cost * overtime_used[w]) -
                     (material_cost * (regular_baskets[w] + overtime_baskets[w])) -
                     (holding_cost * inventory[w]) for w in range(1, W + 1)])

problem += profit

# Constraints
for w in range(1, W + 1):
    # Production Capacity Constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w - 1] + overtime_labor[w - 1]
    
    # Basket Assembly Constraints
    problem += regular_baskets[w] * assembly_time <= regular_used[w]
    problem += overtime_baskets[w] * assembly_time <= overtime_used[w]
    
    # Demand Satisfaction Constraints
    if w > 1:
        problem += regular_baskets[w] + overtime_baskets[w] + inventory[w - 1] == demand[w - 1] + inventory[w]
    
    # Initial inventory condition
    if w == 1:
        problem += inventory[1] == 0

# Salvage Value Condition
problem += inventory[W] >= 0  # Inventory at week W incurs salvage value

# Non-negativity Constraints are inherently handled by lowBound=0 in variable declarations

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')