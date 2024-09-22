import pulp
import json

# Data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(T)]

# Objective function
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
             pulp.lpSum(switch_cost * abs(x[i] - x[i-1]) for i in range(1, T)) + \
             pulp.lpSum(x[i] for i in range(T))

problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += inventory[i] == x[i] - deliver[i], f"Inventory_Constraint_{i}"
    else:
        problem += inventory[i] == inventory[i-1] + x[i] - deliver[i], f"Inventory_Constraint_{i}"

# Solve the problem
problem.solve()

# Extract results
x_values = [pulp.value(x[i]) for i in range(T)]
cost = pulp.value(problem.objective)

# Output
output = {"x": x_values, "cost": cost}
print(output)
print(f' (Objective Value): <OBJ>{cost}</OBJ>')