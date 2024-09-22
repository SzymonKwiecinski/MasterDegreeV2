import pulp

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

# Parameters
W = len(data['demand'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
regular_used = pulp.LpVariable.dicts("regular_used", range(W), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("overtime_used", range(W), lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts("regular_basket", range(W), lowBound=0, cat='Continuous')
overtime_basket = pulp.LpVariable.dicts("overtime_basket", range(W), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(W+1), lowBound=0, cat='Continuous')

# Objective Function
profit = (
    pulp.lpSum(
        (data['selling_price'] - data['material_cost']) * (regular_basket[w] + overtime_basket[w])
        - data['regular_cost'] * regular_used[w]
        - data['overtime_cost'] * overtime_used[w]
        - data['holding_cost'] * inventory[w]
        for w in range(W)
    )
    + data['salvage_value'] * inventory[W]
)

problem += profit

# Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]
    problem += regular_basket[w] == regular_used[w] / data['assembly_time']
    problem += overtime_basket[w] == overtime_used[w] / data['assembly_time']
    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] + inventory[0] == data['demand'][w] + inventory[w]
    else:
        problem += regular_basket[w] + overtime_basket[w] + inventory[w-1] == data['demand'][w] + inventory[w]

# Initial inventory
problem += inventory[0] == 0

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')