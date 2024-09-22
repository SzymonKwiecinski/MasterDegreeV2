import pulp
import json

# Input data
data = {'T': 12, 
        'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 
        'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Production_Inventory_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
             pulp.lpSum(switch_cost * abs(x[i] - x[i + 1]) for i in range(T - 1)) + \
             pulp.lpSum(x[i] for i in range(T)) # production cost, if any
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] + inventory[i] >= deliver[i], f"Delivery_Constraint_{i}"
    else:
        problem += x[i] + inventory[i] + inventory[i - 1] >= deliver[i], f"Delivery_Constraint_{i}"
    
    if i < T - 1:
        problem += inventory[i] >= 0, f"Inventory_Non_Negativity_{i}"

# Solve the problem
problem.solve()

# Retrieve results
production_plan = [x[i].varValue for i in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output results
output = {
    "x": production_plan,
    "cost": total_cost_value
}

print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')