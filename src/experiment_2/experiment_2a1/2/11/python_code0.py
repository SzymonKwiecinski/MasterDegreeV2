import pulp
import json

data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Extracting data from the input
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
             pulp.lpSum(switch_cost * abs(x[i] - x[i + 1]) for i in range(T - 1)) + \
             pulp.lpSum(x[i] for i in range(T))  # total production to meet demands
objective = pulp.lpSum(total_cost)
problem += objective 

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliveries[i] + inventory[i] == 0  # first month
    else:
        problem += x[i] - deliveries[i] + inventory[i] == inventory[i - 1]  # subsequent months

# Ending inventory has no value
problem += inventory[T - 1] == 0

# Solve the problem
problem.solve()

# Collect results
production_schedule = [x[i].varValue for i in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output format
output = {
    "x": production_schedule,
    "cost": total_cost_value,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')