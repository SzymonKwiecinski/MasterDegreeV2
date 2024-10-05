import pulp

# Input data
data = {
    'T': 12, 
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    'StorageCost': 5, 
    'SwitchCost': 10
}

# Extract data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_and_Inventory", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, T+1), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(0, T), lowBound=0, cat='Continuous')

# Objective function
total_cost = (pulp.lpSum(storage_cost * inventory[i] for i in range(T)) +
               pulp.lpSum(switch_cost * (x[i+1] - x[i]) for i in range(1, T) if x[i+1] >= x[i]) +
               pulp.lpSum(switch_cost * (x[i] - x[i+1]) for i in range(1, T) if x[i+1] < x[i]))

problem += total_cost

# Constraints
problem += (inventory[0] == 0, "Initial_Inventory")
for i in range(1, T+1):
    if i < T:
        problem += (x[i] + inventory[i-1] == deliver[i-1] + inventory[i], f"Delivery_Constraint_{i}")
    else:
        problem += (x[i] + inventory[i-1] == deliver[i-1], f"Delivery_Constraint_{i}")

# Solve the problem
problem.solve()

# Output
output = {
    "x": [pulp.value(x[i]) for i in range(1, T+1)],
    "cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')