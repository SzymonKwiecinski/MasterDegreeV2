import pulp
import json

# Data input
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

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

# Decision Variables
problem = pulp.LpProblem("Fine_Foods_Profit_Maximization", pulp.LpMaximize)

regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

# Objective Function
profit = pulp.lpSum((selling_price - material_cost) * (regular_basket[w] + overtime_basket[w]) -
                    regular_cost * regular_used[w] - overtime_cost * overtime_used[w] -
                    holding_cost * inventory[w] for w in range(W))
profit += salvage_value * inventory[W-1]  # Add salvage value for inventory of last week
problem += profit

# Constraints
for w in range(W):
    # Labor constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w] + overtime_labor[w]
    
    # Production constraints
    problem += regular_basket[w] + overtime_basket[w] <= (regular_used[w] / assembly_time + 
                                                           overtime_used[w] / assembly_time)
    
    # Demand satisfaction
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] >= demand[w]  # Inventory 0 at week 0
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] >= demand[w]
    
    # Inventory balance
    if w == 0:
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - demand[w]
    else:
        problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - demand[w]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')