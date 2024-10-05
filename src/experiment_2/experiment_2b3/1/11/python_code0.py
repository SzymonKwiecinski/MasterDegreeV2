import pulp

# Read data
data = {
    'T': 12, 
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    'StorageCost': 5, 
    'SwitchCost': 10
}

T = data['T']
Deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the problem
problem = pulp.LpProblem("Production_Inventory_Planning", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum([
    storage_cost * inventory[i] for i in range(T)
]) + pulp.lpSum([
    switch_cost * pulp.lpAbs(x[i+1] - x[i]) for i in range(T-1)
])

problem += total_cost

# Constraints
# Inventory balance constraints
problem += (x[0] - Deliver[0] == inventory[0], "Inventory_Balance_0")
for i in range(1, T):
    problem += (x[i] - Deliver[i] + inventory[i-1] == inventory[i], f"Inventory_Balance_{i}")

# Initial inventory is zero
problem += (inventory[0] == 0, "Initial_Inventory")

# Solve the problem
problem.solve()

# Extract the results
production_plan = [pulp.value(x[i]) for i in range(T)]

# Calculate the total cost
total_cost_value = pulp.value(problem.objective)

# Print results
output = {
    "x": production_plan,
    "cost": total_cost_value
}
print(output)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')