import pulp
import json

# Data
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')

# Parameters
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Variables
x = pulp.LpVariable.dicts('x', range(1, T + 1), lowBound=0)  # Production levels
I = pulp.LpVariable.dicts('I', range(1, T + 1), lowBound=0)  # Inventory levels

# Problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + pulp.lpSum(switch_cost * (x[i] - x[i + 1]) for i in range(1, T))

# Constraints
I[1] = x[1] - deliver[0]  # Inventory for the first month
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1]  # Inventory balance constraint

# Non-negativity constraints
for i in range(1, T + 1):
    problem += x[i] >= 0
    problem += I[i] >= 0

# Solve the problem
problem.solve()

# Output production levels and total cost
production_levels = [x[i].varValue for i in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

# Print results
print(f'Production Levels: {production_levels}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')