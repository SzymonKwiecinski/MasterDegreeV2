import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]  # production in month i
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(T)]  # inventory at end of month i

# Objective function
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
             pulp.lpSum(switch_cost * abs(x[i] - x[i+1]) for i in range(T-1)) + \
             pulp.lpSum(x[i] for i in range(T))  # total production cost (not explicitly in the problem but is implied)
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliveries[i] + inventory[i] == 0  # initial month (no previous inventory)
    else:
        problem += x[i] + inventory[i-1] - deliveries[i] + inventory[i] == 0

# Solve the problem
problem.solve()

# Prepare the output
results = {
    "x": [x[i].varValue for i in range(T)],
    "cost": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{results["cost"]}</OBJ>')