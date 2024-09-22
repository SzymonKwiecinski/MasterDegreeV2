import pulp
import json

data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Production_Inventory_Schedule", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
            pulp.lpSum(switch_cost * abs(x[i] - x[i+1]) for i in range(T-1)) + \
            pulp.lpSum(x[i] for i in range(T)), "Total_Cost"

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] + inventory[i] == deliver[i], f"Demand_Constraint_{i}"
    else:
        problem += x[i] + inventory[i] == deliver[i] + inventory[i-1], f"Demand_Constraint_{i}"

# Solve the problem
problem.solve()

# Collect results
results = {
    "x": [x[i].varValue for i in range(T)],
    "cost": pulp.value(problem.objective)
}

print(json.dumps(results))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')