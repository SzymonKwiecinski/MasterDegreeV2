import pulp
import json

# Input data from JSON
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Extract variables from data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([storage_cost * inventory[i] for i in range(T)]) + \
           pulp.lpSum([switch_cost * pulp.lpAbs(x[i] - x[i-1]) for i in range(1, T)])

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] + inventory[i] == deliver[i], f"Initial_Inventory{0}"
    else:
        problem += x[i] + inventory[i] == deliver[i] + inventory[i-1], f"Inventory_Constraint{i}"

# Solve the problem
problem.solve()

# Prepare the output
result_x = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

# Output format
output = {
    "x": result_x,
    "cost": cost,
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{cost}</OBJ>')