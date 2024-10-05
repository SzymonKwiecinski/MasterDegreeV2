import pulp

# Define data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Extract variables
T = data['T']
Deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Initialize the LP problem
problem = pulp.LpProblem("Production_Inventory_Planning", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (i for i in range(1, T + 1)), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", (i for i in range(1, T + 1)), lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum([
    storage_cost * inventory[i] + 
    switch_cost * pulp.lpSum([x[i] - x[i-1] for i in range(2, T + 1)])
    for i in range(1, T + 1)
])

# Constraints
problem += inventory[1] == x[1] - Deliver[0]  # For the first month
for i in range(1, T):
    problem += inventory[i + 1] == inventory[i] + x[i + 1] - Deliver[i]

# Solve the problem
problem.solve()

# Collect results
production_plan = [pulp.value(x[i]) for i in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

# Print results
print({
    "x": production_plan,
    "cost": total_cost
})
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')