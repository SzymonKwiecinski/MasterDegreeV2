import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

# Extracting values from the data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(T), lowBound=0, cat='Continuous')

# Objective Function
total_cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)]) + \
             pulp.lpSum([switch_cost * abs(x[i] - x[i+1]) for i in range(T - 1)]) + \
             pulp.lpSum(x[i] for i in range(T))
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] + inventory[i] == 0
    else:
        problem += x[i] - deliver[i] + inventory[i] == inventory[i - 1]

# Solve the problem
problem.solve()

# Collect the results
x_values = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

# Output result
result = {"x": x_values, "cost": cost}
print(result)
print(f' (Objective Value): <OBJ>{cost}</OBJ>')