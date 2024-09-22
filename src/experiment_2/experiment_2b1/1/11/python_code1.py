import pulp
import json

data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Extract the data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_Inventory_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)]) + \
             pulp.lpSum([switch_cost * (x[i] - x[i + 1])**2 for i in range(T - 1)])**0.5 # Using squared difference to avoid abs()
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += (x[i] - deliver[i] + inventory[i] == 0)  # First month constraint
    else:
        problem += (x[i] - deliver[i] + inventory[i] + inventory[i - 1] == 0)  # Transition constraint
    if i < T - 1:
        problem += (inventory[i] >= 0)  # Non-negativity constraint for inventory

# Solve the problem
problem.solve()

# Prepare the output
x_values = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

output = {
    "x": x_values,
    "cost": cost,
}

print(f' (Objective Value): <OBJ>{cost}</OBJ>')