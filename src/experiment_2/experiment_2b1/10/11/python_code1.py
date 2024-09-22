import pulp
import json

# Input data
data = {'T': 12, 
        'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 
        'SwitchCost': 10}

T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
           pulp.lpSum(switch_cost * (x[i+1] - x[i]) for i in range(T-1) if x[i+1] >= x[i]) + \
           pulp.lpSum(switch_cost * (x[i] - x[i+1]) for i in range(T-1) if x[i] > x[i+1]), "Total_Cost"

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] + inventory[i] == deliveries[i], f"Balance_Constraint_{i}"
    else:
        problem += x[i] + inventory[i] + inventory[i-1] == deliveries[i], f"Balance_Constraint_{i}"

# Solve the problem
problem.solve()

# Extracting results
productions = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

# Output format
output = {
    "x": productions,
    "cost": cost,
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{cost}</OBJ>')