import pulp
import json

# Load data
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, '
                  '"material_cost": 25, "selling_price": 65, "holding_cost": 4, '
                  '"salvage_value": 30, "demand": [700, 1500, 2800, 1800], '
                  '"regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

# Parameters
W = len(data['demand'])
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
assembly_time = data['assembly_time']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

# Problem
problem = pulp.LpProblem("Fine_Foods_Company", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("regular_used", range(W), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("overtime_used", range(W), lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts("regular_basket", range(W), lowBound=0, cat='Continuous')
overtime_basket = pulp.LpVariable.dicts("overtime_basket", range(W), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(W), lowBound=0, cat='Continuous')

# Objective Function
profit_terms = [(selling_price - material_cost - holding_cost) * (regular_basket[w] + overtime_basket[w]) -
                regular_cost * regular_used[w] - overtime_cost * overtime_used[w] for w in range(W)]
profit_terms.append(salvage_value * inventory[W-1])
problem += pulp.lpSum(profit_terms), "Total Profit"

# Constraints
for w in range(W):
    # Demand Satisfaction
    if w == 0:
        problem += (regular_basket[w] + overtime_basket[w] + 0 == demand[w] + inventory[w], f"Demand_Satisfaction_week_{w+1}")
    else:
        problem += (regular_basket[w] + overtime_basket[w] + inventory[w-1] == demand[w] + inventory[w], f"Demand_Satisfaction_week_{w+1}")

    # Labor Hour Constraints
    problem += (regular_used[w] <= regular_labor[w], f"Regular_Labor_Constraint_week_{w+1}")
    problem += (overtime_used[w] <= overtime_labor[w], f"Overtime_Labor_Constraint_week_{w+1}")
    problem += (regular_used[w] + overtime_used[w] >= assembly_time * (regular_basket[w] + overtime_basket[w]), f"Labor_Assembly_Constraint_week_{w+1}")

# Solve Problem
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')