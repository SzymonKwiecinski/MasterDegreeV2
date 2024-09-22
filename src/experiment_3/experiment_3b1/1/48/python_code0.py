import pulp

# Data from the JSON format
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
selling_price = data['selling_price']
material_cost = data['material_cost']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
holding_cost = data['holding_cost']
assembly_time = data['assembly_time']

# Initialize the problem
problem = pulp.LpProblem("Fine_Foods_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), 0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), 0)
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(W), 0, None, pulp.LpInteger)
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(W), 0, None, pulp.LpInteger)
inventory = pulp.LpVariable.dicts("Inventory", range(W), 0)

# Objective Function
total_profit = pulp.lpSum(
    (selling_price * (regular_baskets[w] + overtime_baskets[w]) -
     material_cost * (regular_baskets[w] + overtime_baskets[w]) -
     regular_cost * regular_used[w] -
     overtime_cost * overtime_used[w] -
     holding_cost * inventory[w]) for w in range(W)
)

problem += total_profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]
    problem += regular_used[w] + overtime_used[w] >= assembly_time * (regular_baskets[w] + overtime_baskets[w])
    
    if w > 0:
        problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w]
    else:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - data['demand'][w]

# Initial inventory constraint
problem += inventory[0] == 0 

# Last week inventory does not incur holding cost
# No additional constraint is needed as it is implicitly handled

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')