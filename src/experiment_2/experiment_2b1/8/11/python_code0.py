import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Extracting variables from data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Production_and_Inventory", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(T)]

# Objective Function
total_cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)]) + \
             pulp.lpSum([switch_cost * abs(x[i] - x[i+1]) for i in range(T-1)])

problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] + inventory[i] == 0  # Initial month, no prior inventory
    else:
        problem += x[i] - deliver[i] + inventory[i] == inventory[i-1]  # Inventory carried over

# Solve the problem
problem.solve()

# Gather results
production_schedule = [pulp.value(x[i]) for i in range(T)]
total_cost_value = pulp.value(problem.objective)

# Format output
output = {
    "x": production_schedule,
    "cost": total_cost_value,
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')