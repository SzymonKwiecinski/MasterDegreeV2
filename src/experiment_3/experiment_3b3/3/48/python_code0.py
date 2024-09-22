import pulp

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

W = len(data['demand'])  # Number of weeks

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("regular_used", range(1, W+1), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("overtime_used", range(1, W+1), lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts("regular_basket", range(1, W+1), lowBound=0, cat='Continuous')
overtime_basket = pulp.LpVariable.dicts("overtime_basket", range(1, W+1), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(1, W+1), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([
    (
        data['selling_price'] * (regular_basket[w] + overtime_basket[w]) -
        data['regular_cost'] * regular_used[w] -
        data['overtime_cost'] * overtime_used[w] -
        data['material_cost'] * (regular_basket[w] + overtime_basket[w]) -
        data['holding_cost'] * inventory[w]
    ) for w in range(1, W+1)
]) + data['salvage_value'] * inventory[W]

problem += profit

# Constraints
for w in range(1, W+1):
    # Regular labor constraint
    problem += regular_used[w] <= data['regular_labor'][w-1]

    # Overtime labor constraint
    problem += overtime_used[w] <= data['overtime_labor'][w-1]

    # Labor hour constraint for basket assembly
    problem += (regular_basket[w] + overtime_basket[w]) / data['assembly_time'] <= regular_used[w] + overtime_used[w]

# Demand fulfillment
for w in range(2, W+1):
    problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] - inventory[w] == data['demand'][w-1]

# Initial inventory
problem += inventory[1] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')