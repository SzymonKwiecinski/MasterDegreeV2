import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

# Parameters setup
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create a linear programming problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
           pulp.lpSum(switch_cost * abs(x[i] - x[i-1]) for i in range(1, T)) + \
           pulp.lpSum(x[i] for i in range(T)), "Total_Cost"

# Constraints
for i in range(T):
    problem += inventory[i-1] + x[i] - deliveries[i] == inventory[i] if i > 0 else x[i] - deliveries[i] == inventory[i]

# Solving the problem
problem.solve()

# Preparing output
output = {
    "x": [x[i].varValue for i in range(T)],
    "cost": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{output["cost"]}</OBJ>')