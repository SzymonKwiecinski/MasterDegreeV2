import pulp
import json

# Data
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

# Problem Definition
W = len(data['demand'])
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("Regular_Baskets", range(W), lowBound=0, cat='Integer')
overtime_baskets = pulp.LpVariable.dicts("Overtime_Baskets", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum([data['selling_price'] * (regular_baskets[w] + overtime_baskets[w]) - 
                     data['material_cost'] * (regular_baskets[w] + overtime_baskets[w]) for w in range(W)]) - \
    pulp.lpSum([data['regular_cost'] * regular_used[w] + data['overtime_cost'] * overtime_used[w] for w in range(W)]) - \
    pulp.lpSum([data['holding_cost'] * inventory[w] for w in range(W - 1)]) + \
    data['salvage_value'] * inventory[W - 1]

problem += profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]
    problem += regular_baskets[w] == regular_used[w] / data['assembly_time']
    problem += overtime_baskets[w] == overtime_used[w] / data['assembly_time']
    
    if w > 0:
        problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w]
    else:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - data['demand'][w]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')